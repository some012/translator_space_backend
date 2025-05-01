from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File

from app.config.auth.current_user import get_current_user
from app.config.db.s3.schemas import ViewUrlSchemaOut
from app.config.db.s3.service import S3Service
from app.config.logger import logger
from app.enums.s3 import S3BucketName
from app.schemas.user import UserRole, UserUpdate
from app.services.user_service import UserService
from app.utils.helpers.file_helper import file_helper

router = APIRouter()


@router.get("/me")
async def get_me(
    current_user: Annotated[UserRole, Depends(get_current_user)],
) -> UserRole:
    return current_user


@router.post("/img")
async def add_image(
    current_user: Annotated[UserRole, Depends(get_current_user)],
    s3_service: S3Service.register_deps(),
    user_service: UserService.register_deps(),
    file: UploadFile = File(...),
) -> ViewUrlSchemaOut:
    logger.info(f"Validate {file.filename}")
    file_helper.validate_image_file(file=file)

    source_bytes = await file.read()

    await s3_service.upload(file, source_bytes, S3BucketName.IMAGES)

    logger.info("Start update user in db")
    current_user.img = file.filename
    user_in = UserUpdate(**current_user.__dict__)
    await user_service.update_user(user_sid=current_user.sid, update_user=user_in)
    logger.info("Finish update user in db")

    img_url = await s3_service.generate_view_url(
        s3_object_path=file.filename, s3_bucket=S3BucketName.IMAGES
    )

    await file.close()

    return ViewUrlSchemaOut(url=img_url)


@router.get("/img")
async def get_image(
    current_user: Annotated[UserRole, Depends(get_current_user)],
    s3_service: S3Service.register_deps(),
) -> ViewUrlSchemaOut:
    img_url = await s3_service.generate_view_url(
        s3_object_path=current_user.img, s3_bucket=S3BucketName.IMAGES
    )
    return ViewUrlSchemaOut(url=img_url)
