from fastapi import APIRouter
from app.api.v1.endpoints import (
        prompt_optimizer,
)

api_router = APIRouter()

api_router.include_router(prompt_optimizer.router, prefix="/prompt-optimizer", tags=["Prompt Optimizer"])


