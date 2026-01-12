"""
Conjure Utils - API wrappers for Gemini and Meshy
"""

import base64
import os
import time

import requests


def get_client(api_key):
    """Create a Gemini client."""
    from google import genai

    return genai.Client(api_key=api_key)


def refine_prompt(api_key, prompt):
    """Use Gemini to refine a prompt for 3D model generation."""
    client = get_client(api_key)

    instruction = (
        f"Refine this prompt for generating a high-quality 3D model reference image. "
        f"Only generate a frontal view of the object. "
        f"Other views will be generated later again using this as the original "
        f"reference image, so this must be a perfect visualization of the original "
        f"objective."
        f"Adhere to the use of a white background, product shot setting. "
        f"Object: {prompt}. Return ONLY the refined prompt, no markdown."
    )

    response = client.models.generate_content(
        model="gemini-3-pro-preview", contents=instruction
    )
    return response.text.strip()


def generate_image(api_key, prompt, output_path, input_image_path=None):
    """
    Generate an image using Gemini.
    If input_image_path is provided, use it as reference for the generation.
    """
    from google.genai import types
    from PIL import Image

    client = get_client(api_key)

    config = types.GenerateContentConfig(
        response_modalities=["Image"],
        image_config=types.ImageConfig(aspect_ratio="1:1"),
    )

    if input_image_path:
        ref_image = Image.open(input_image_path)
        contents = [prompt, ref_image]
    else:
        contents = prompt

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=contents,
        config=config,
    )

    for part in response.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            img = part.as_image()
            img.save(output_path)
            return output_path

    raise Exception("No image in response")


def generate_3d_meshy(api_key, image_paths):
    """
    Generate 3D model from images using Meshy Multi-Image API.
    Accepts a single path or list of paths.
    """
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # Convert images to data URIs
    image_urls = []
    for path in image_paths:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(path)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        image_urls.append(f"data:{mime};base64,{encoded}")

    payload = {
        "image_urls": image_urls,
        "ai_model": "meshy-5",
        "topology": "triangle",
        "target_polycount": 75000,
        "should_remesh": True,
        "should_texture": False,
    }

    # Create task - API returns 202 Accepted on success
    resp = requests.post(
        "https://api.meshy.ai/openapi/v1/multi-image-to-3d",
        headers=headers,
        json=payload,
    )

    # 200 or 202 are both success
    if resp.status_code not in [200, 202]:
        raise Exception(f"Meshy API error {resp.status_code}: {resp.text}")

    task_id = resp.json()["result"]

    # Poll until complete
    for _ in range(120):
        time.sleep(5)
        status_resp = requests.get(
            f"https://api.meshy.ai/openapi/v1/multi-image-to-3d/{task_id}",
            headers=headers,
        )
        if status_resp.status_code != 200:
            continue

        data = status_resp.json()
        if data["status"] == "SUCCEEDED":
            return data["model_urls"]["glb"]
        elif data["status"] in ["FAILED", "EXPIRED"]:
            msg = data.get("task_error", {}).get("message", "Unknown error")
            raise Exception(f"Meshy failed: {msg}")

    raise Exception("Meshy timed out")


def download_file(url, output_path):
    """Download a file from URL."""
    # ⚡ Bolt: Stream download to reduce memory usage for large files
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path
