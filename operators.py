import bpy
import threading
import tempfile
import queue
from . import utils


class CONJURE_OT_Generate(bpy.types.Operator):
    bl_idname = "conjure.generate_all"
    bl_label = "Generate 3D Object"
    bl_description = "Generate a 3D object from text prompt"
    
    _timer = None
    _thread = None
    _queue = None
    
    def modal(self, context, event):
        if event.type != 'TIMER':
            return {'PASS_THROUGH'}
        
        tool = context.scene.conjure
        
        # Process all queued messages
        while not self._queue.empty():
            msg = self._queue.get_nowait()
            msg_type, text, path = msg
            
            if msg_type == 'DONE':
                tool.is_running = False
                context.window_manager.event_timer_remove(self._timer)
                return {'FINISHED'}
            
            if msg_type == 'ERROR':
                tool.is_running = False
                self.report({'ERROR'}, text)
                context.window_manager.event_timer_remove(self._timer)
                return {'CANCELLED'}
            
            if msg_type == 'REFINED':
                tool.refined_prompt = text
            
            if msg_type == 'IMPORT':
                self._import_model(path)
            
            # Add to log
            log = tool.logs.add()
            log.message = text
            log.type = 'IMAGE' if msg_type == 'IMAGE' else 'INFO'
            log.path = path
        
        # Force UI redraw
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        
        return {'PASS_THROUGH'}
    
    def _import_model(self, filepath):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.gltf(filepath=filepath)
    
    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences
        
        if not prefs.gemini_api_key or not prefs.meshy_api_key:
            self.report({'ERROR'}, "Set API keys in addon preferences")
            return {'CANCELLED'}
        
        tool = context.scene.conjure
        tool.logs.clear()
        tool.is_running = True
        tool.refined_prompt = ""
        
        self._queue = queue.Queue()
        self._thread = threading.Thread(
            target=self._run_pipeline,
            args=(prefs.gemini_api_key, prefs.meshy_api_key, tool.prompt, self._queue)
        )
        self._thread.start()
        
        self._timer = context.window_manager.event_timer_add(0.3, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def _run_pipeline(self, gemini_key, meshy_key, prompt, q):
        try:
            q.put(('INFO', "Refining prompt...", ""))
            
            # Step 1: Refine prompt
            refined = utils.refine_prompt(gemini_key, prompt)
            q.put(('REFINED', refined, ""))
            q.put(('INFO', "Prompt refined", ""))
            
            # Step 2: Generate views
            views = [
                ("Front", f"Front view of {refined}, white background, product shot"),
                ("Right", f"Right side view of {refined}, white background, product shot"),
                ("Back", f"Back view of {refined}, white background, product shot"),
                ("Left", f"Left side view of {refined}, white background, product shot"),
            ]
            
            image_paths = []
            front_path = None
            
            for view_name, view_prompt in views:
                q.put(('INFO', f"Generating {view_name}...", ""))
                
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                    out_path = f.name
                
                # Use front image as reference for other views
                ref_image = front_path if front_path else None
                path = utils.generate_image(gemini_key, view_prompt, out_path, ref_image)
                
                if view_name == "Front":
                    front_path = path
                
                image_paths.append(path)
                q.put(('IMAGE', f"{view_name} done", path))
            
            # Step 3: Generate 3D
            q.put(('INFO', "Uploading to Meshy...", ""))
            model_url = utils.generate_3d_meshy(meshy_key, image_paths)
            
            # Step 4: Download
            q.put(('INFO', "Downloading model...", ""))
            with tempfile.NamedTemporaryFile(suffix=".glb", delete=False) as f:
                model_path = f.name
            utils.download_file(model_url, model_path)
            
            # Step 5: Import
            q.put(('IMPORT', "Importing model...", model_path))
            q.put(('INFO', "Complete!", ""))
            q.put(('DONE', "", ""))
            
        except Exception as e:
            q.put(('ERROR', str(e), ""))


def register():
    bpy.utils.register_class(CONJURE_OT_Generate)


def unregister():
    bpy.utils.unregister_class(CONJURE_OT_Generate)
