from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

from app.config.auth.current_user import get_current_user
from app.config.logger import logger
from app.enums.file import ContentType
from app.parsing.ts.ts import ts_format_parser
from app.schemas.file import FileCreate, FileLines
from app.schemas.line import LineCreate
from app.services.file_service import FileService
from app.services.line_service import LineService
from app.services.project_service import ProjectService
from app.utils.custom_options.file_options import FileCustomOptions
from app.utils.helpers.file_helper import file_helper

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/upload/{project_sid}")
async def upload_translation_file(
    project_sid: UUID,
    file_service: FileService.register_deps(),
    project_service: ProjectService.register_deps(),
    line_service: LineService.register_deps(),
    file: UploadFile = File(...),
) -> FileLines:
    logger.info(f"Validate {file.filename}")
    file_helper.validate_file(file=file)
    logger.info("Check existence of project")
    project = await project_service.get_one_project(project_sid=project_sid)

    if not project:
        logger.warning("Project not found")
        raise HTTPException(status_code=404, detail="Проект не найден!")

    logger.info("Start create file in db")
    source_bytes = await file.read()
    file_in = FileCreate(
        project_sid=project_sid, name=file.filename, source_bytes=source_bytes
    )
    file_db = await file_service.create_file(file_in=file_in)
    file_sid = file_db.sid
    logger.info("Finish create file in db")

    logger.info("Parse a ts file to json")
    ts_json = await ts_format_parser.from_ts_to_json(source_bytes)

    logger.info("Add file with lines to db")
    all_lines_db = []
    for lines in ts_json["contexts"]:
        for group, lines in lines.items():
            for line in lines:
                line_in = LineCreate(
                    file_sid=file_db.sid,
                    meaning=line["source"],
                    translation=line["translation"],
                    translated=True,
                    group=group,
                    filename=line["filename"],
                    line=line["line"],
                )
                all_lines_db.append(line_in)

    await line_service.create_from_list(list_lines=all_lines_db)
    logger.info("Created file in db")

    return await file_service.get_one_file(
        file_sid=file_sid, custom_options=FileCustomOptions.with_lines()
    )


@router.post("/create/{sid}")
async def create_translation_file(
    sid: UUID,
    file_service: FileService.register_deps(),
):
    logger.info("Get file from db")
    file = await file_service.get_one_file(
        file_sid=sid, custom_options=FileCustomOptions.with_lines()
    )

    if not file:
        logger.warning("File not found")
        raise HTTPException(status_code=404, detail="Файл не найден в базе!")

    logger.info("Parse list lines to file")
    modified_file = await ts_format_parser.from_list_to_ts(
        lines=file.lines, file_content=file.source_bytes, file_name=file.name
    )
    logger.info("Return created file")
    return StreamingResponse(
        modified_file.file,
        media_type=ContentType.TS,
        headers={
            "Content-Disposition": f"attachment; filename={modified_file.filename}"
        },
    )
