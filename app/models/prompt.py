from beanie import Document
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.common import LogBase


class PromptAnalysis(BaseModel):
    intent: Optional[str] = None
    clarity_score: Optional[float] = None

    role_missing: Optional[bool] = None
    constraints_missing: Optional[bool] = None
    output_format_missing: Optional[bool] = None

    detected_issues: Optional[List[str]] = []
    improvement_suggestions: Optional[List[str]] = []

class OptimizedPrompt(BaseModel):
    version: int
    prompt: str

class PromptOptimization(LogBase):
    user_id:Optional[str]=None
    original_prompt: str
    
    analysis: Optional[PromptAnalysis] = None
    
    optimized_prompts: List[OptimizedPrompt] = None

    model_used: Optional[str] = None
    provider: Optional[str] = None  # openai / gemini / claude

    language: Optional[str] = None
    category: Optional[str] = None  # seo / coding / writing

    class Settings:
        name = "prompt_optimizations"
