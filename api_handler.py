import requests

STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

def generate_ai_image(prompt: str, api_key: str):
    """
    Handles secure image data streams from the Stability AI Core Engine.
    """
    headers = {
        "authorization": f"Bearer {api_key}",
        "accept": "image/*"
    }
    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
        "aspect_ratio": (None, "1:1")
    }
    try:
        response = requests.post(STABILITY_URL, headers=headers, files=files, timeout=45)
        if response.status_code == 401:
            return None, "❌ AUTHORIZATION FAULT: The API token provided is invalid or out of credits."
        elif response.status_code != 200:
            return None, f"❌ SERVER FAULT: {response.text}"
        return response.content, None
    except Exception as e:
        return None, f"❌ CONNECTION ERROR: {str(e)}"