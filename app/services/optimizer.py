from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel
from typing import List

from app.prompts.optimizer import OPTIMIZER_SYSTEM_PROMPT, OPTIMIZER_HUMAN_PROMPT
from app.models.prompt import PromptAnalysis, OptimizedPrompt
from app.utils.json_utils import extract_json


class OptimizerResponse(BaseModel):
    optimized_prompts: List[OptimizedPrompt]


class PromptOptimizerService:
    def __init__(self, llm):
        prompt = ChatPromptTemplate.from_messages([
            ("system", OPTIMIZER_SYSTEM_PROMPT),
            ("human", OPTIMIZER_HUMAN_PROMPT),
        ])

        # LCEL pipeline
        self.chain = prompt | llm | StrOutputParser()

    async def optimize(
        self,
        original_prompt: str,
        analysis: PromptAnalysis
    ) -> List[OptimizedPrompt]:

        response = await self.chain.ainvoke({
            "original_prompt": original_prompt,
            "analysis_json": analysis.model_dump_json()
        })
        
        clean_json = extract_json(response)

        parsed = OptimizerResponse.model_validate_json(clean_json)
        return parsed.optimized_prompts
