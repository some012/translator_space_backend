from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.config.auth.current_user import get_current_user
from app.config.logger import logger
from app.schemas.project import (
    ProjectCreate,
    Project,
    ProjectAdd,
    ProjectAll,
    ProjectUpdate,
)
from app.schemas.user import UserRole
from app.services.project_service import ProjectService
from app.utils.custom_options.project_options import ProjectCustomOptions

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post(path="/add")
async def create_project(
    project_create: ProjectCreate,
    project_service: ProjectService.register_deps(),
    current_user: Annotated[UserRole, Depends(get_current_user)],
) -> Project:
    project_in = ProjectAdd(**project_create.__dict__, user_sid=current_user.sid)
    logger.info("Begin create project")
    project = await project_service.create_project(project_in=project_in)
    logger.info("Successfully created project")
    return project


@router.get(path="/{sid}")
async def get_one_project(
    sid: UUID,
    project_service: ProjectService.register_deps(),
    is_extented: bool = False,
) -> Project | ProjectAll | None:
    if is_extented:
        logger.info("Get extended project")
        project = await project_service.get_one_project(
            project_sid=sid, custom_options=ProjectCustomOptions.with_files_and_lines()
        )
    else:
        logger.info("Get project")
        project = await project_service.get_one_project(project_sid=sid)

    if not project:
        logger.warning("Project not found")
        raise HTTPException(status_code=404, detail="Проект не найден!")

    return project


@router.get(path="s")
async def get_all_projects(
    project_service: ProjectService.register_deps(), is_extented: bool = False
) -> List[Project | ProjectAll]:
    if is_extented:
        logger.info("Get extended projects")
        return await project_service.get_all_projects(
            custom_options=ProjectCustomOptions.with_files_and_lines()
        )
    logger.info("Get projects")
    return await project_service.get_all_projects()


@router.put(path="/update/{sid}")
async def update_one_project(
    sid: UUID,
    update_project: ProjectUpdate,
    project_service: ProjectService.register_deps(),
) -> Project | None:
    project = await project_service.get_one_project(project_sid=sid)

    if not project:
        logger.warning("Project not found")
        raise HTTPException(status_code=404, detail="Проект не найден!")

    logger.info("Update project")
    updated_project = await project_service.update_project(
        project_sid=sid, update_project=update_project
    )
    logger.info("Successfully updated project")
    return updated_project


@router.delete(path="/delete/{sid}")
async def delete_one_project(
    sid: UUID,
    project_service: ProjectService.register_deps(),
):
    project = await project_service.get_one_project(project_sid=sid)

    if not project:
        logger.warning("Project not found")
        raise HTTPException(status_code=404, detail="Проект не найден!")

    logger.info("Delete project")
    await project_service.delete_project(project_sid=sid)
    logger.info("Successfully deleted project")
    return HTTPException(status_code=200, detail="Проект успешно удален!")
