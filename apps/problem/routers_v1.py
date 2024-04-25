from .router import router as problems_router

routers = ({"router": problems_router, "extra_params": {"tags": ("problems", )}}, )

__all__ = ('routers', )
