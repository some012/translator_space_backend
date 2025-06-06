from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi_pagination.iterables import LimitOffsetPage, paginate

from app.config.auth.current_user import get_current_active_user
from app.config.db.s3.schemas import ViewUrlSchemaOut, MessageResponseSchemaOut
from app.config.db.s3.service import S3Service
from app.config.logger import logger
from app.enums.s3 import S3BucketName, S3FolderName
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
from app.utils.helpers.file_helper import file_helper

router = APIRouter()


@router.post(path="/add/", dependencies=[Depends(get_current_active_user)])
async def create_project(
    project_create: ProjectCreate,
    project_service: ProjectService.register_deps(),
    current_user: Annotated[UserRole, Depends(get_current_active_user)],
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


@router.get(path="s/")
async def get_all_projects(
    project_service: ProjectService.register_deps(),
) -> LimitOffsetPage[Project]:
    logger.info("Get projects")
    results = await project_service.get_all_projects()
    return paginate(results)


@router.get(path="/search/")
async def search(
    project_service: ProjectService.register_deps(),
    name: Optional[str] = None,
    description: Optional[str] = None,
    datetime_start: Optional[datetime] = None,
    datetime_end: Optional[datetime] = None,
) -> LimitOffsetPage[Project]:
    results = await project_service.search_projects(
        name=name,
        description=description,
        datetime_start=datetime_start,
        datetime_end=datetime_end,
    )
    return paginate(results)


@router.put(path="/update/{sid}", dependencies=[Depends(get_current_active_user)])
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
        project=project, update_project=update_project
    )
    logger.info("Successfully updated project")
    return updated_project


@router.delete(path="/delete/{sid}", dependencies=[Depends(get_current_active_user)])
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


@router.post("/{sid}/img/", dependencies=[Depends(get_current_active_user)])
async def add_image(
    sid: UUID,
    s3_service: S3Service.register_deps(),
    project_service: ProjectService.register_deps(),
    file: UploadFile = File(...),
) -> ViewUrlSchemaOut:
    logger.info(f"Validate {file.filename}")
    file_helper.validate_image_file(file=file)

    source_bytes = await file.read()

    project = await project_service.get_one_project(project_sid=sid)

    if not project:
        logger.warning("Project not found")
        raise HTTPException(status_code=404, detail="Проект не найден!")

    logger.info("Start update project in db")
    project.img = file.filename
    project_in = ProjectUpdate(**project.__dict__)
    await project_service.update_project(project=project, update_project=project_in)
    logger.info("Finish update project in db")

    logger.info("Upload file to S3")
    await s3_service.upload(
        file=file,
        source_bytes=source_bytes,
        s3_bucket_name=S3BucketName.IMAGES,
        s3_folder_name=S3FolderName.PROJECT,
    )
    logger.info("Uploaded file to S3")

    s3_object_path = s3_service.generate_upload_path_with_folder_name(
        s3_object_file_name=project.img, s3_folder_name=S3FolderName.PROJECT
    )

    logger.info("Generate view url for access to front")
    img_url = await s3_service.generate_view_url(
        s3_object_path=s3_object_path, s3_bucket=S3BucketName.IMAGES
    )
    logger.info("View url generated")

    await file.close()

    return ViewUrlSchemaOut(url=img_url)


@router.get("/{sid}/img/", dependencies=[Depends(get_current_active_user)])
async def get_image(
    sid: UUID,
    s3_service: S3Service.register_deps(),
    project_service: ProjectService.register_deps(),
) -> ViewUrlSchemaOut:
    project = await project_service.get_one_project(project_sid=sid)

    if not project:
        logger.warning("Project not found")
        raise HTTPException(status_code=404, detail="Проект не найден!")

    s3_object_path = s3_service.generate_upload_path_with_folder_name(
        s3_object_file_name=project.img, s3_folder_name=S3FolderName.PROJECT
    )

    logger.info("Get image from s3")
    img_url = await s3_service.generate_view_url(
        s3_object_path=s3_object_path, s3_bucket=S3BucketName.IMAGES
    )
    return ViewUrlSchemaOut(url=img_url)


@router.delete("/{sid}/img/", dependencies=[Depends(get_current_active_user)])
async def delete_image(
    sid: UUID,
    s3_service: S3Service.register_deps(),
    project_service: ProjectService.register_deps(),
) -> MessageResponseSchemaOut:
    project = await project_service.get_one_project(project_sid=sid)

    if not project:
        logger.warning("Project not found")
        raise HTTPException(status_code=404, detail="Проект не найден!")

    s3_object_path = s3_service.generate_upload_path_with_folder_name(
        s3_object_file_name=project.img, s3_folder_name=S3FolderName.PROJECT
    )
    logger.info("Delete image from s3")
    await s3_service.remove_digital_object(
        s3_object_path=s3_object_path, s3_bucket=S3BucketName.IMAGES
    )

    logger.info("Start update project in db")
    project.img = None
    project_in = ProjectUpdate(**project.__dict__)
    await project_service.update_project(project=project, update_project=project_in)
    logger.info("Finish update project in db")

    logger.info("Finish delete image from s3")
    return MessageResponseSchemaOut(message="Image has been deleted")
