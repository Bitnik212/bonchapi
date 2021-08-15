from fastapi import APIRouter, Form, Header, Query, UploadFile, File

from bonch.msg import BonchMessage
from server.app.errors.ServerErrors.FilesErrors import FilesErrors
from server.core.utils.ResponseBuilder import ResponseBuilder

router = APIRouter(
    prefix="/files"
)


@router.post(
    path="/load",
    tags=["Файлы"],
    summary="Загрузить файл",
    responses=FilesErrors().errors
)
async def load_file(
        miden: str = Header(
            ...,
            description="Токен для доступа к лк",
            alias="X-Token-Miden",
            min_length=32,
            max_length=34
        ),
        file_name: str = Form(..., description="Название файла", alias="fileName"),
        file: UploadFile = File(..., description="Файл"),
        idinfo: int = Form(0, description="Id сообщения к которому добавить файл")
):
    bonch = BonchMessage(miden)
    file_bytes = await file.read()
    file_raw = bonch.upload_file(file=file_bytes, file_name=file_name, id=idinfo)
    if file_raw[0] != 200:
        return ResponseBuilder().result(status=file_raw[0], info=file_raw[1], data={})
    else:
        return ResponseBuilder().result(status=file_raw[0], data=file_raw[1])
