from app.routers.analytics import router as analytics_router
from app.routers.auth import router as auth_router
from app.routers.categories import router as categories_router
from app.routers.expenses import router as expenses_router

__all__ = ["auth_router", "expenses_router", "categories_router", "analytics_router"]
