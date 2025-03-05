from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from app.config.auth.current_user import get_current_user
from app.config.logger import logger
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
    file_in = FileCreate(project_sid=project_sid, name=file.filename)
    file_db = await file_service.create_file(file_in=file_in)
    file_sid = file_db.sid
    logger.info("Finish create file in db")

    logger.info("Parse a ts file to json")
    ts_json = await ts_format_parser.from_ts_to_json(file)

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
