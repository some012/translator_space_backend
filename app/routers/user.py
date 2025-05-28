import json
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Body
from starlette import status
from starlette.responses import JSONResponse

from app.config.auth.current_user import get_current_active_user
from app.config.auth.password_schema import ChangePassword, ResetPassword
from app.config.consts.msg import Msg
from app.config.db.redis.session import redis_conn
from app.config.db.s3.schemas import ViewUrlSchemaOut, MessageResponseSchemaOut
from app.config.db.s3.service import S3Service
from app.config.logger import logger
from app.config.settings import project_settings
from app.enums.s3 import S3BucketName
from app.schemas.user import UserUpdate, UserRole, UserActivity
from app.services.user_service import UserService
from app.utils.helpers.file_helper import file_helper

router = APIRouter()


@router.get("/me/")
async def get_me(
    current_user: Annotated[UserRole, Depends(get_current_active_user)],
) -> UserRole:
    return current_user


@router.put(path="/me")
async def update_user_me(
    user_in: Annotated[UserUpdate, Depends()],
    current_user: Annotated[UserRole, Depends(get_current_active_user)],
    user_service: UserService.register_deps(),
) -> UserRole:
    return await user_service.update_user(
        user_sid=current_user.sid,
        user_in=user_in,
    )


@router.delete("/remove")
async def remove_me(
    current_user: Annotated[UserRole, Depends(get_current_active_user)],
    user_service: UserService.register_deps(),
) -> JSONResponse:
    await user_service.soft_delete_user_by_sid(user_sid=current_user.sid)
    return JSONResponse(
        content=Msg(msg="Удалено").model_dump(), status_code=status.HTTP_200_OK
    )


@router.patch("/change_password")
async def change_password(
    data: Annotated[ChangePassword, Body()],
    current_user: Annotated[UserRole, Depends(get_current_active_user)],
    user_service: UserService.register_deps(),
) -> JSONResponse:
    return await user_service.change_user_password(
        user_sid=current_user.sid,
        new_password=data.new_password,
        old_password=data.old_password,
        myself=True,
    )


@router.patch(path="/reset_password", response_model=Msg)
async def reset_password(
    data: Annotated[ResetPassword, Body()],
    current_user: Annotated[UserRole, Depends(get_current_active_user)],
    user_service: UserService.register_deps(),
) -> JSONResponse:
    return await user_service.reset_user_password(
        user_sid=current_user.sid, new_password=data.new_password
    )


@router.get("/activity")
async def get_count_activity_user(
    current_user: Annotated[UserRole, Depends(get_current_active_user)],
) -> UserActivity:
    key_date = f"{current_user.sid}:date_activity"
    key_count = f"{current_user.sid}:activity"

    logger.info("Get last activity user from redis")
    last_date_str, count_str = await redis_conn.mget(key_date, key_count)
    today = datetime.utcnow().date()

    if last_date_str and count_str:
        last_date_json = json.loads(last_date_str)
        count_json = json.loads(count_str)
        last_date = datetime.strptime(last_date_json["date"], "%Y-%m-%d").date()
        count = int(count_json["count"]) if count_str else 1

        if last_date == today:
            logger.info("Same day in last activity, nothing changed")
            pass
        elif today == last_date + timedelta(days=1):
            logger.info("User's activity detected")
            count += 1
        else:
            count = 1
    else:
        logger.info("First visit of user")
        count = 1

    logger.info("Save data of last activity in redis")
    await redis_conn.setex(
        name=key_date,
        time=project_settings.ACTIVITY_COUNT_EXPIRE_SECONDS,
        value=json.dumps({"date": str(current_user.last_activity.date())}),
    )

    await redis_conn.setex(
        name=key_count,
        time=project_settings.ACTIVITY_COUNT_EXPIRE_SECONDS,
        value=json.dumps({"count": count}),
    )

    logger.info("Get count activity of current user")
    return UserActivity(sid=current_user.sid, count=count)


@router.post("/img/")
async def add_image(
    current_user: Annotated[UserRole, Depends(get_current_active_user)],
    s3_service: S3Service.register_deps(),
    user_service: UserService.register_deps(),
    file: UploadFile = File(...),
) -> ViewUrlSchemaOut:
    logger.info(f"Validate {file.filename}")
    file_helper.validate_image_file(file=file)

    source_bytes = await file.read()

    logger.info("Upload file to S3")
    await s3_service.upload(file, source_bytes, S3BucketName.IMAGES)
    logger.info("Uploaded file to S3")

    logger.info("Start update user in db")
    current_user.img = file.filename
    user_in = UserUpdate(**current_user.__dict__)
    await user_service.update_user(user_sid=current_user.sid, update_user=user_in)
    logger.info("Finish update user in db")

    logger.info("Generate view url for access to front")
    img_url = await s3_service.generate_view_url(
        s3_object_path=file.filename, s3_bucket=S3BucketName.IMAGES
    )
    logger.info("View url generated")

    await file.close()

    return ViewUrlSchemaOut(url=img_url)


@router.get("/img/")
async def get_image(
    current_user: Annotated[UserRole, Depends(get_current_active_user)],
    s3_service: S3Service.register_deps(),
) -> ViewUrlSchemaOut:
    logger.info("Get image from s3")
    img_url = await s3_service.generate_view_url(
        s3_object_path=current_user.img, s3_bucket=S3BucketName.IMAGES
    )
    return ViewUrlSchemaOut(url=img_url)


@router.delete("/img/")
async def delete_image(
    current_user: Annotated[UserRole, Depends(get_current_active_user)],
    s3_service: S3Service.register_deps(),
) -> MessageResponseSchemaOut:
    logger.info("Delete image from s3")
    await s3_service.remove_digital_object(
        s3_object_path=current_user.img, s3_bucket=S3BucketName.IMAGES
    )
    logger.info("Finish delete image from s3")
    return MessageResponseSchemaOut(message="Image has been deleted")
