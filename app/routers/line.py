from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.config.auth.current_user import get_current_active_user
from app.config.logger import logger
from app.schemas.line import (
    Line,
    LineUpdate,
    ChangeLine,
    TranslationMLLine,
)
from app.services.file_service import FileService
from app.services.line_service import LineService
from app.services.translation.translation_service import TranslationService
from app.utils.custom_options.line_options import LineCustomOptions

router = APIRouter()


@router.get(path="/{sid}")
async def get_one_line(
    sid: UUID,
    line_service: LineService.register_deps(),
) -> Line | None:
    logger.info("Get line")
    line = await line_service.get_one_line(line_sid=sid)

    if not line:
        logger.warning("Line not found")
        raise HTTPException(status_code=404, detail="Строка не найдена!")

    return line


@router.get(path="s/")
async def get_all_lines(line_service: LineService.register_deps()) -> List[Line]:
    logger.info("Get lines")
    return await line_service.get_all_lines()


@router.get(path="/by-file/{sid}")
async def get_all_lines_by_file(
    sid: UUID, line_service: LineService.register_deps()
) -> List[Line]:
    logger.info("Get lines from file")
    return await line_service.get_all_lines_by_file_sid(file_sid=sid)


@router.post(
    path="/generate-translation/{sid}", dependencies=[Depends(get_current_active_user)]
)
async def generate_translation_for_line(
    sid: UUID,
    line_service: LineService.register_deps(),
    translation_service: TranslationService.register_deps(),
) -> ChangeLine:
    line = await line_service.get_one_line(
        line_sid=sid, custom_options=LineCustomOptions.with_file()
    )

    if not line:
        logger.warning("Line not found")
        raise HTTPException(status_code=404, detail="Строка не найдена!")

    translation_ml = await translation_service.translate(
        texts=line.meaning, language=line.file.translate_language
    )

    return ChangeLine(meaning=line.meaning, translation=translation_ml[0])


@router.post(
    path="/generate-translation/by-file/{sid}",
    dependencies=[Depends(get_current_active_user)],
)
async def generate_translation_for_many_lines(
    sid: UUID,
    file_service: FileService.register_deps(),
    line_service: LineService.register_deps(),
    translation_service: TranslationService.register_deps(),
) -> list[TranslationMLLine]:
    file = await file_service.get_one_file(file_sid=sid)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    lines = await line_service.get_all_lines_by_file_sid(file_sid=sid)

    all_translation_meanings = []
    all_translation_sids = []

    for line in lines:
        all_translation_meanings.append(line.meaning)
        all_translation_sids.append(line.sid)

    translation_ml = await translation_service.translate(
        texts=all_translation_meanings, language=file.translate_language
    )

    all_translations = []

    for index, meaning in enumerate(all_translation_meanings):
        changed_line = TranslationMLLine(
            sid=all_translation_sids[index],
            meaning=meaning,
            translation=translation_ml[index],
        )
        all_translations.append(changed_line)

    return all_translations


@router.put(path="/update/{sid}", dependencies=[Depends(get_current_active_user)])
async def update_one_line(
    sid: UUID,
    change_line: ChangeLine,
    line_service: LineService.register_deps(),
) -> Line | None:
    line = await line_service.get_one_line(line_sid=sid)

    if not line:
        logger.warning("Line not found")
        raise HTTPException(status_code=404, detail="Строка не найдена!")

    line.meaning = change_line.meaning
    line.translation = change_line.translation

    update_line = LineUpdate(**line.__dict__)

    logger.info("Update line")
    updated_line = await line_service.update_line(line=line, update_line=update_line)
    logger.info("Successfully updated line")
    return updated_line


@router.delete(path="/delete/{sid}", dependencies=[Depends(get_current_active_user)])
async def delete_one_line(
    sid: UUID,
    line_service: LineService.register_deps(),
):
    line = await line_service.get_one_line(line_sid=sid)

    if not line:
        logger.warning("Line not found")
        raise HTTPException(status_code=404, detail="Строка не найдена!")

    logger.info("Delete line")
    await line_service.delete_line(line_sid=sid)
    logger.info("Successfully deleted line")
    return HTTPException(status_code=200, detail="Строка успешно удалена!")
