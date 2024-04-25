from .router import router as users_router

routers = ({"router": users_router, "extra_params": {"tags": ("problems",)}},)

__all__ = ("routers",)
