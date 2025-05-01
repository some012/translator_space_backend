import os

from fastapi import UploadFile, HTTPException

from app.enums.file import ContentType, TranslationFileFormat, ImageFileFormat


class FileHelper:
    def validate_tranlation_file(self, file: UploadFile) -> None:
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in TranslationFileFormat:
            raise HTTPException(status_code=400, detail="Неверное расширение файла")

        if file.content_type not in ContentType:
            raise HTTPException(status_code=400, detail="Неверный формат файла")

    def validate_image_file(self, file: UploadFile) -> None:
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ImageFileFormat:
            raise HTTPException(status_code=400, detail="Неверное расширение файла")


file_helper = FileHelper()
