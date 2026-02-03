# frontend/base_llm.py

from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings


def generate_llm_response(user_message: str) -> str:
    """
    Acts like ChatGPT / Gemini chat.
    Returns RAW model outputs.
    """

    llm = ChatGoogleGenerativeAI(
        google_api_key=settings.GEMINI_API_KEY,
        model=settings.GEMINI_MODEL,
        temperature=0.6
    )

    response = llm.invoke(user_message)
    return response.content
