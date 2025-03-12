from typing import Annotated, Sequence
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.config.logger import logger
from app.deps.db import get_db
from app.models import ProjectModel
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.repositories.file_repository import FileRepository
from app.services.repositories.line_repository import LineRepository
from app.services.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, db: AsyncSession):
        self._project_repository = ProjectRepository(db=db)
        self._line_repository = LineRepository(db=db)
        self._file_repository = FileRepository(db=db)

    async def create_project(self, project_in: ProjectCreate) -> ProjectModel:
        return await self._project_repository.create(c_obj=project_in)

    async def update_project(
        self, project_sid: UUID, update_project: ProjectUpdate
    ) -> ProjectModel:
        project = await self._project_repository.get_one(sid=project_sid)

        if project is None:
            raise HTTPException(status_code=400, detail="Project not found")

        return await self._project_repository.update(
            db_obj=project, u_obj=update_project
        )

    async def get_one_project(
        self,
        project_sid: UUID,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> ProjectModel | None:
        return await self._project_repository.get_one(
            sid=project_sid, custom_options=custom_options
        )

    async def get_by_name(self, name: str) -> ProjectModel | None:
        return await self._project_repository.get_by_name(name=name)

    async def get_all_projects(
        self,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> Sequence[ProjectModel]:
        return await self._project_repository.get_all(custom_options=custom_options)

    async def delete_project(self, project_sid: UUID):
        logger.info("Get all files by this project sid")
        all_files_sids = await self._file_repository.get_many_by_project_sid(
            project_sid=project_sid, only_sids=True
        )

        logger.info("Delete all lines in files")
        for sid in all_files_sids:
            await self._line_repository.delete_all_by_file_sid(file_sid=sid)

        logger.info("Delete all files")
        await self._file_repository.delete_all_by_project_sid(project_sid=project_sid)

        logger.info("Delete project")
        return await self._project_repository.delete(sid=project_sid)

    @staticmethod
    def register(db: AsyncSession):
        return ProjectService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[ProjectService, Depends(get_project_service)]


async def get_project_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return ProjectService(db=db)
