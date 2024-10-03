from fastapi import APIRouter

from app.routers import role, auth

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Auth"], prefix="/auth")
api_router.include_router(role.router, tags=["Role"], prefix="/role")
