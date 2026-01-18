from pydantic import BaseModel, Field
from typing import List


class PromptOptimizeCreate(BaseModel):
    prompt: str = Field(..., min_length=5)
    provider: str = Field(default="openai")


class OptimizedPromptResponse(BaseModel):
    version: int
    prompt: str


class PromptOptimizeResponse(BaseModel):
    original_prompt: str
    optimized_prompts: List[OptimizedPromptResponse]
