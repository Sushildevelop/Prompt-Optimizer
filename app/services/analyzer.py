from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.prompts.analyzer import (
    ANALYZER_SYSTEM_PROMPT,
    ANALYZER_HUMAN_PROMPT
)
from app.models.prompt import PromptAnalysis
from app.utils.json_utils import extract_json



class PromptAnalyzerService:
    def __init__(self, llm):
        prompt = ChatPromptTemplate.from_messages([
            ("system", ANALYZER_SYSTEM_PROMPT),
            ("human", ANALYZER_HUMAN_PROMPT),
        ])

        # LCEL pipeline (future-proof)
        self.chain = prompt | llm | StrOutputParser()

    async def analyze(self, user_prompt: str) -> PromptAnalysis:
        """
        Analyze user prompt and return structured PromptAnalysis
        """
        response = await self.chain.ainvoke({
            "user_prompt": user_prompt
        })
        clean_json = extract_json(response)

        return PromptAnalysis.model_validate_json(clean_json)
