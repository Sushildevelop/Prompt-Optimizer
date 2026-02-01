# frontend/optimizer_api.py

import requests

OPTIMIZER_URL = "http://localhost:8000/api/v1/prompt-optimizer"


def optimize_raw_prompt(raw_text: str) -> dict:
    """
    Sends raw model output to Prompt Optimizer backend.
    """
    response = requests.post(
        OPTIMIZER_URL,
        data=raw_text.encode("utf-8"),
        headers={"Content-Type": "text/plain"},
        timeout=60
    )

    response.raise_for_status()
    return response.json()
