# frontend/optimizer_api.py

import requests

OPTIMIZER_URL = "http://localhost:8000/api/v1/prompt-optimizer"


def optimize_raw_prompt(raw_text: str) -> dict:
    """
    Sends raw model output to Prompt Optimizer backend.
    """
    payload = {
        "prompt": raw_text,
        "provider": "groq"  # You can make this configurable later
    }

    response = requests.post(
        OPTIMIZER_URL,
        json=payload,  # Send as JSON instead of raw text
        headers={"Content-Type": "application/json"},
        timeout=60
    )

    response.raise_for_status()
    return response.json()
