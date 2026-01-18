from langchain_google_genai import ChatGoogleGenerativeAI
# Future providers (keep commented for now)
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
from app.core.config import settings

def get_llm(provider: str = "gemini"):
    """
    LLM factory method.
    Default provider: Gemini
    """

    provider = provider.lower()

    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            google_api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_MODEL,
            temperature=0.3,
            convert_system_message_to_human=True
        )

    # ---- Future Providers ----
    # elif provider == "openai":
    #     return ChatOpenAI(
    #         api_key=settings.OPENAI_API_KEY,
    #         model=settings.OPENAI_MODEL,
    #         temperature=0.3
    #     )

    # elif provider == "claude":
    #     return ChatAnthropic(
    #         api_key=settings.CLAUDE_API_KEY,
    #         model=settings.CLAUDE_MODEL,
    #         temperature=0.3
    #     )

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
