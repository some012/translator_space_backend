from fastapi import APIRouter

from app.routers import auth, admin, project

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Auth"], prefix="/auth")
api_router.include_router(admin.router, tags=["Admin"], prefix="/admin")

api_router.include_router(project.router, tags=["Project"], prefix="/project")
