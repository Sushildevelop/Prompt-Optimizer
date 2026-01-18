from fastapi import APIRouter, Depends, HTTPException, status,BackgroundTasks
# from app.models.user import User
# from app.api.deps import get_current_manager_or_admin_user
from app.schemas.prompt_optimizer import (
    PromptOptimizeCreate,
    PromptOptimizeResponse
)
from app.services.prompt_optimizer import PromptOptimizerFacadeService
from app.utils.logger import app_logger
from app.models.prompt import PromptOptimization



async def save_prompt_optimization(data: dict):
    db_obj = PromptOptimization(**data)
    await db_obj.insert()

router = APIRouter()


@router.post("", response_model=PromptOptimizeResponse)
async def optimize_prompt(
    payload: PromptOptimizeCreate,
    background_tasks:BackgroundTasks,
    # current_user: User = Depends(get_current_manager_or_admin_user),
):
    """
    Analyze a prompt and generate 5 optimized prompt versions
    """
    try:
        result = await PromptOptimizerFacadeService.optimize_prompt(
            prompt=payload.prompt,
            provider=payload.provider,
            # user_id=str(current_user.id)
        )
        background_tasks.add_task(
            save_prompt_optimization,
            result
        )
        return {
            "original_prompt": result["original_prompt"],
            "optimized_prompts": result["optimized_prompts"]
        }

    except ValueError as e:
        app_logger.warning(f"Prompt optimizer validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        app_logger.exception("Unexpected error during prompt optimization")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
