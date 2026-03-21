from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
# Future providers (keep commented for now)
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
from app.core.config import settings

def get_llm(provider: str = "groq"):
    """
    LLM factory method.
    Default provider: Gemini
    """

    provider = provider.lower()

    if provider == "groq":
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0.6
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
