from .router import router as playground_router

routers = ({"router": playground_router, "extra_params": {"tags": ("playground", )}}, )

__all__ = ('routers', )
