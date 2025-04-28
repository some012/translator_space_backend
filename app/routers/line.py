from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.config.auth.current_user import get_current_user
from app.config.logger import logger
from app.schemas.line import (
    Line,
    LineUpdate,
    ChangeLine,
)
from app.services.line_service import LineService

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(path="/{sid}")
async def get_one_line(
    sid: UUID,
    line_service: LineService.register_deps(),
) -> Line | None:
    logger.info("Get line")
    line = await line_service.get_one_line(line_sid=sid)

    if not line:
        logger.warning("Line not found")
        raise HTTPException(status_code=404, detail="Строка не найден!")

    return line


@router.get(path="s")
async def get_all_lines(line_service: LineService.register_deps()) -> List[Line]:
    logger.info("Get lines")
    return await line_service.get_all_lines()


@router.get(path="/by-file/{sid}")
async def get_all_lines_by_file(
    sid: UUID, line_service: LineService.register_deps()
) -> List[Line]:
    logger.info("Get lines from file")
    return await line_service.get_all_lines_by_file_sid(file_sid=sid)


@router.put(path="/update/{sid}")
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
    updated_line = await line_service.update_line(line_sid=sid, update_line=update_line)
    logger.info("Successfully updated line")
    return updated_line


@router.delete(path="/delete/{sid}")
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
