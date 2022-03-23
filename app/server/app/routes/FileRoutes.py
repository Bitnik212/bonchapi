from fastapi import APIRouter, Form, Header, Query, UploadFile, File

from bonch import Settings
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
        miden=Settings.miden_key.value,
        file_name: str = Form(..., description="Название файла", alias="fileName"),
        file: UploadFile = File(..., description="Файл"),
        idinfo: int = Form(0, description="Id сообщения к которому добавить файл")
):
    bonch = BonchMessage(miden)
    file_bytes = await file.read()
    file_raw = bonch.upload_file(file=file_bytes, file_name=file_name, id=idinfo)
    if file_raw[0] != 200:
        return ResponseBuilder().result(status=file_raw[0], info=file_raw[1], data=None)
    else:
        return ResponseBuilder().result(status=file_raw[0], data=file_raw[1])
