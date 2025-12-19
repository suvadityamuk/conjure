# Conjure - Blender Add-on

A [Blender](https://www.blender.org/) add-on that uses AI to generate 3D objects from text prompts!

## Workflow
1.  [**Gemini 3**](https://ai.google.dev/gemini-api/docs/gemini-3): Refines your simple text prompt into a detailed description. Uses Gemini 3 Pro.
2.  [**Nano-Banana Pro**](https://gemini.google/overview/image-generation/): Generates a high-quality reference image from the refined prompt along with 3 more reference images from different angles.
3.  [**Meshy.ai**](https://meshy.ai): Converts the reference image into a 3D model (.glb) and imports it into Blender.

## Installation

1.  Open Blender.
2.  Go to `Edit > Preferences > Add-ons`.
3.  Click `Install...` and select the `conjure_addon` folder (or zip it first).
    *   *Note: If installing as a folder doesn't work, zip the `conjure_addon` directory into `conjure_addon.zip` and install that.*
4.  Enable the add-on "Conjure 3D AI".
5.  Enter your API keys for Gemini and Meshy.ai in the add-on settings.
6.  Click `Install Dependencies` to install the required Python dependencies.

## Blender Add-On Store

Watch this space! Once the add-on is approved, we will update this space with instructions to download the extension from the [Blender Extensions Store](https://extensions.blender.org/add-ons/) directly.

## Dependencies

This add-on requires the `requests` and `google-genai` Python libraries. Install them into your Blender Python environment by going to `Edit > Preferences > Add-ons > Conjure > Install Dependencies`.

In the future, we will move to bundle these dependencies in the extension itself to remove this manual step. More [details here](https://docs.blender.org/manual/en/dev/advanced/extensions/addons.html#bundle-dependencies).

## Usage

1.  Open the 3D Viewport.
2.  Press `N` to open the sidebar.
3.  Click on the **Conjure** tab.
4.  Type your prompt (e.g., "A magical potion bottle").
5.  Click **Generate 3D Object**.
6.  Wait for the process to complete (check the Status tab for more).

## Paid Components Disclaimer

1. The Gemini API uses `gemini-3-pro-preview`, which is a paid API, to refine the prompt.
2. The Gemini 3 Pro Image preview (Nano Banana Pro) model is then used to generate multi-view images of the object. This generates 4 images.
3. The Meshy.ai API is then used to generate a 3D model from the images. This is a paid API as well.

## Configuration

*   **Gemini API**: Uses Google Generative AI.
*   **Nano-Banana**: Currently configured to use a placeholder generator for demonstration if a private endpoint is not set. You can edit `utils.py` to point to your specific Nano-Banana endpoint.
*   **Meshy**: Requires a valid Meshy.ai API key.

## Demo Video

Click [here](assets/conjure_demo_2-5x.mp4) to watch the demo video. Note that this video is sped up 2.5x for the sake of brevity.

## Contributing

Please feel free to refer to #1 to contribute to this project. We welcome all kinds of contributions, such as improving the docs or adding more models and coverage.

## License

Apache License 2.0
