from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db
from app.services.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, db: AsyncSession):
        self._project_repository = ProjectRepository(db=db)

    @staticmethod
    def register(db: AsyncSession):
        return ProjectService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[ProjectService, Depends(get_project_service)]


async def get_project_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return ProjectService(db=db)
