import re


def extract_json(text: str) -> str:
    """
    Extract JSON from LLM output.
    Handles markdown fences and stray text.
    """

    text = text.strip()

    # Case 1: ```json ... ```
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*", "", text)
        text = re.sub(r"```$", "", text)
        return text.strip()

    # Case 2: text before/after JSON
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0).strip()

    # Fallback: return as-is (will fail validation)
    return text
