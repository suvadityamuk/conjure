import concurrent.futures
import queue
import tempfile
import threading

import bpy

from . import utils


class CONJURE_OT_Generate(bpy.types.Operator):
    bl_idname = "conjure.generate_all"
    bl_label = "Generate 3D Object"
    bl_description = "Generate a 3D object from text prompt"

    _timer = None
    _thread = None
    _queue = None

    def modal(self, context, event):
        if event.type != "TIMER":
            return {"PASS_THROUGH"}

        tool = context.scene.conjure

        # Process all queued messages
        refresh_needed = False
        while not self._queue.empty():
            refresh_needed = True
            msg = self._queue.get_nowait()
            msg_type, text, path = msg

            if msg_type == "DONE":
                tool.is_running = False
                context.window_manager.event_timer_remove(self._timer)
                return {"FINISHED"}

            if msg_type == "ERROR":
                tool.is_running = False
                self.report({"ERROR"}, text)
                context.window_manager.event_timer_remove(self._timer)
                return {"CANCELLED"}

            if msg_type == "REFINED":
                tool.refined_prompt = text

            if msg_type == "IMPORT":
                self._import_model(path)

            # Add to log
            log = tool.logs.add()
            log.message = text
            log.type = "IMAGE" if msg_type == "IMAGE" else "INFO"
            log.path = path

        # Force UI redraw
        if refresh_needed:
            for area in context.screen.areas:
                if area.type == "VIEW_3D":
                    area.tag_redraw()

        return {"PASS_THROUGH"}

    def _import_model(self, filepath):
        bpy.ops.object.select_all(action="DESELECT")
        bpy.ops.import_scene.gltf(filepath=filepath)

    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences

        if not prefs.gemini_api_key or not prefs.meshy_api_key:
            self.report({"ERROR"}, "Set API keys in addon preferences")
            return {"CANCELLED"}

        tool = context.scene.conjure
        tool.logs.clear()
        tool.is_running = True
        tool.refined_prompt = ""

        self._queue = queue.Queue()
        self._thread = threading.Thread(
            target=self._run_pipeline,
            args=(prefs.gemini_api_key, prefs.meshy_api_key, tool.prompt, self._queue),
        )
        self._thread.start()

        self._timer = context.window_manager.event_timer_add(0.3, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def _run_pipeline(self, gemini_key, meshy_key, prompt, q):
        try:
            # ⚡ Bolt: Create client once to save ~80ms per call
            client = utils.get_client(gemini_key)

            q.put(("INFO", "Refining prompt...", ""))

            # Step 1: Refine prompt
            refined = utils.refine_prompt(gemini_key, prompt, client=client)
            q.put(("REFINED", refined, ""))
            q.put(("INFO", "Prompt refined", ""))

            # Step 2: Generate Front View (Synchronous - needed as reference)
            q.put(("INFO", "Generating Front view...", ""))

            front_prompt = f"Front view of {refined}, white background, product shot"

            # Helper to generate a single view
            def generate_view(view_name, view_prompt, input_ref=None, client=None):
                q.put(("INFO", f"Generating {view_name}...", ""))
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
                    out = tf.name

                # If it's the front view call, input_ref is None usually,
                # but valid for subsequent calls
                res_path = utils.generate_image(
                    gemini_key, view_prompt, out, input_ref, client=client
                )
                q.put(("IMAGE", f"{view_name} done", res_path))
                return res_path

            # Generate front view first
            front_path = generate_view("Front", front_prompt, None, client=client)

            # Step 3: Generate Other Views (Parallel)
            remaining_views = [
                (
                    "Right",
                    f"Right side view of {refined}, white background, product shot",
                ),
                ("Back", f"Back view of {refined}, white background, product shot"),
                (
                    "Left",
                    f"Left side view of {refined}, white background, product shot",
                ),
            ]

            # We need to maintain order: Front, Right, Back, Left for Meshy?
            # Meshy docs say "image_urls": [front, right, back, left, top, bottom]
            # usually, but order technically doesn't strictly matter for multicam
            # unless specified.
            # However, `image_paths` list was ordered before. Let's keep it ordered.

            image_paths = [front_path]

            # Re-doing the parallel part to be cleaner and maintain order
            # We can map the futures directly
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                # Submit tasks in order
                futures = []
                for v_name, v_prompt in remaining_views:
                    futures.append(
                        executor.submit(
                            generate_view, v_name, v_prompt, front_path, client
                        )
                    )

                # Gather results in order
                results = [f.result() for f in futures]
                image_paths.extend(results)

            # Step 3: Generate 3D
            q.put(("INFO", "Uploading to Meshy...", ""))
            model_url = utils.generate_3d_meshy(meshy_key, image_paths)

            # Step 4: Download
            q.put(("INFO", "Downloading model...", ""))
            with tempfile.NamedTemporaryFile(suffix=".glb", delete=False) as f:
                model_path = f.name
            utils.download_file(model_url, model_path)

            # Step 5: Import
            q.put(("IMPORT", "Importing model...", model_path))
            q.put(("INFO", "Complete!", ""))
            q.put(("DONE", "", ""))

        except Exception as e:
            q.put(("ERROR", str(e), ""))


def register():
    bpy.utils.register_class(CONJURE_OT_Generate)


def unregister():
    bpy.utils.unregister_class(CONJURE_OT_Generate)
