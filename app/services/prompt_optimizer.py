from app.services.analyzer import PromptAnalyzerService
from app.services.optimizer import PromptOptimizerService
from app.services.llm_factory import get_llm
from app.models.prompt import PromptOptimization
from app.core.config import settings


class PromptOptimizerFacadeService:
    """
    Facade service that orchestrates:
    Analyzer → Optimizer → DB storage
    """

    @staticmethod
    async def optimize_prompt(
        prompt: str,
        provider: str,
    ):
        # 1. Load LLM
        llm = get_llm(provider)

        # Get model name from settings based on provider
        provider_upper = provider.upper()
        model_used = getattr(settings, f"{provider_upper}_MODEL", f"{provider}_default_model")
        provider_used = provider.lower()

        # 2. Analyze prompt
        analyzer = PromptAnalyzerService(llm)
        analysis = await analyzer.analyze(prompt)

        # 3. Optimize prompt
        optimizer = PromptOptimizerService(llm)
        optimized_prompts = await optimizer.optimize(
            original_prompt=prompt,
            analysis=analysis
        )

        # 4. Save to MongoDB


        # 5. Return response
        return {
            "original_prompt": prompt,
            "analysis": analysis,
            "optimized_prompts": optimized_prompts,
            "provider": provider_used,
            "model_used": model_used
            # "created_by": user_id
        }
