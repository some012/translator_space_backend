import os
from datetime import timedelta
from io import BytesIO
from typing import Annotated, Optional

from fastapi import Depends, UploadFile, HTTPException
from minio import Minio
from minio import S3Error
from urllib3 import ProxyManager

from app.config.settings import project_settings
from app.enums.s3 import S3BucketName, S3FolderName


class S3Service:
    minio_client: Minio
    tmp_path: str

    def __init__(self):
        self.minio_client = Minio(
            project_settings.S3_ENDPOINT,
            access_key=project_settings.S3_ACCESS_KEY,
            secret_key=project_settings.S3_SECRET_KEY,
            region=project_settings.S3_REGION,
            secure=project_settings.S3_REQUIRE_TLS,
            http_client=(
                ProxyManager(project_settings.S3_INTERNAL_URL)
                if project_settings.IS_PROXY_REQUIRED
                else None
            ),
        )
        self.tmp_path: str = "./tmp"

    def generate_upload_path_with_file_sid(
        self,
        s3_object_file_name: str,
        file_sid: str,
    ):
        return f"{file_sid}/{s3_object_file_name}"

    def generate_upload_path_with_folder_name(
        self,
        s3_object_file_name: str,
        s3_folder_name: S3FolderName,
    ) -> str:
        return f"{s3_folder_name}/{s3_object_file_name}"

    def __validate_object_existance(
        self, s3_object_path: str, s3_bucket: S3BucketName
    ) -> None:
        try:
            self.minio_client.stat_object(s3_bucket, s3_object_path)
        except S3Error as e:
            if e.code == "NoSuchKey":
                raise HTTPException(
                    status_code=404,
                    detail=f"The file does not exist",
                ) from e
            raise

    async def remove_digital_object(
        self, s3_object_path: str, s3_bucket: S3BucketName
    ) -> None:
        self.__validate_object_existance(
            s3_object_path=s3_object_path, s3_bucket=s3_bucket
        )
        self.minio_client.remove_object(s3_bucket, s3_object_path)

    async def upload(
        self,
        file: UploadFile,
        source_bytes: bytes,
        s3_bucket_name: S3BucketName,
        s3_folder_name: Optional[S3FolderName] = None,
        file_sid: Optional[str] = None,
    ) -> str:
        if s3_bucket_name == S3BucketName.TRANSLATION and file_sid:
            s3_object_path: str = self.generate_upload_path_with_file_sid(
                file.filename, file_sid
            )
        else:
            s3_object_path: str = self.generate_upload_path_with_folder_name(
                file.filename,
                s3_folder_name,
            )
        self.minio_client.put_object(
            bucket_name=s3_bucket_name,
            object_name=s3_object_path,
            data=BytesIO(source_bytes),
            content_type=file.content_type,
            length=len(source_bytes),
        )
        return s3_object_path

    async def download(
        self, s3_object_path: str, s3_bucket: S3BucketName
    ) -> UploadFile:
        self.__validate_object_existance(
            s3_object_path=s3_object_path, s3_bucket=s3_bucket
        )
        file_name = os.path.basename(s3_object_path)

        try:
            response = self.minio_client.get_object(
                bucket_name=s3_bucket,
                object_name=s3_object_path,
            )

            file_bytes = response.read()

            file_like = BytesIO(file_bytes)
            upload_file = UploadFile(filename=file_name, file=file_like)

            return upload_file

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to download file '{s3_object_path}': {str(e)}",
            ) from e

    async def generate_view_url(
        self,
        s3_object_path: str,
        s3_bucket: S3BucketName,
        expiration_minutes: int = 360,
    ) -> str:
        self.__validate_object_existance(
            s3_object_path=s3_object_path, s3_bucket=s3_bucket
        )
        try:
            presigned_url: str = self.minio_client.presigned_get_object(
                bucket_name=s3_bucket,
                object_name=s3_object_path,
                expires=timedelta(minutes=expiration_minutes),
            )
            return presigned_url
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to generate view URL: {str(e)}"
            ) from e

    @staticmethod
    def register():
        return S3Service()

    @staticmethod
    def register_deps():
        return Annotated[S3Service, Depends(get_s3_service)]


async def get_s3_service():
    return S3Service()
