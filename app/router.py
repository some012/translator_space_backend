from fastapi import APIRouter

from app.routers import role

api_router = APIRouter()

api_router.include_router(role.router, tags=["Role"], prefix="/role")
