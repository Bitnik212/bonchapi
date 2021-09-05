from fastapi import APIRouter, Form, Header, Query

from bonch.msg import BonchMessage
from server.app.errors.DefaultErrors import DefaultErrors
from server.app.errors.MessageHistoryErrors import MessageHistoryErrors
from server.app.errors.MessagesErrors import MessagesErrors
from server.core.utils.ResponseBuilder import ResponseBuilder

router = APIRouter(
    prefix="/messages"
)


@router.get(
    path="/in",
    responses=MessagesErrors().errors,
    tags=["Сообщения"],
    summary="Входящие сообщения"
)
async def get_in_messages(
        miden: str = Header(
            ...,
            description="Токен для доступа к лк",
            alias="X-Token-Miden",
            min_length=32,
            max_length=34
        ),
        page_start: int = Query(1, alias="pageStart", description="Получить с такой-то страницы"),
        page_end: int = Query(2, alias="pageEnd", description="Получить до такой-то страницы"),
        page: int = Query(0, alias="page", description="Получить определенную страницу")
):
    """
    Получить входящие сообщения. Если указана страница (page), то pageStart и pageEnd игнорируются
    """
    bonch = BonchMessage(miden)
    messages_raw = bonch.get_messages_in(page_start=page_start, page_end=page_end, page=page)
    if messages_raw[0] != 200:
        return ResponseBuilder().result(data=None, info=messages_raw[1], status=messages_raw[0])
    else:
        return ResponseBuilder().result(data=messages_raw[1], status=messages_raw[0])


@router.get(
    path="/out",
    responses=MessagesErrors().errors,
    tags=["Сообщения"],
    summary="Исходящие сообщения"
)
async def get_out_messages(
        miden: str = Header(
            ...,
            description="Токен для доступа к лк",
            alias="X-Token-Miden",
            min_length=32,
            max_length=34
        ),
        page_start: int = Query(1, alias="pageStart", description="Получить с такой-то страницы"),
        page_end: int = Query(2, alias="pageEnd", description="Получить до такой-то страницы"),
        page: int = Query(0, alias="page", description="Получить определенную страницу")
):
    """
    Получить исходяшие сообщения. Если указана страница (page), то pageStart и pageEnd игнорируются
    """
    bonch = BonchMessage(miden)
    messages_raw = bonch.get_messages_out(page_start=page_start, page_end=page_end, page=page)
    if messages_raw[0] != 200:
        return ResponseBuilder().result(data=None, info=messages_raw[1], status=messages_raw[0])
    else:
        return ResponseBuilder().result(data=messages_raw[1], status=messages_raw[0])


@router.get(
    path="/deleted",
    responses=MessagesErrors().errors,
    tags=["Сообщения"],
    summary="Удаленные сообщения"
)
async def get_delete_messages(
        miden: str = Header(
            ...,
            description="Токен для доступа к лк",
            alias="X-Token-Miden",
            min_length=32,
            max_length=34
        ),
        page_start: int = Query(1, alias="pageStart", description="Получить с такой-то страницы"),
        page_end: int = Query(2, alias="pageEnd", description="Получить до такой-то страницы"),
        page: int = Query(0, alias="page", description="Получить определенную страницу")
):
    """
        Получить удаленные сообщения. Если указана страница (page), то pageStart и pageEnd игнорируются
    """
    bonch = BonchMessage(miden)
    messages_raw = bonch.get_messages_deleted(page_start=page_start, page_end=page_end, page=page)
    if messages_raw[0] != 200:
        return ResponseBuilder().result(data=None, info=messages_raw[1], status=messages_raw[0])
    else:
        return ResponseBuilder().result(data=messages_raw[1], status=messages_raw[0])


@router.post(
    path="/new",
    responses=DefaultErrors().errors,
    tags=["Сообщения"],
    summary="Отправить сообщения"
)
async def new_messages(
        miden: str = Header(
            ...,
            description="Токен для доступа к лк",
            alias="X-Token-Miden",
            min_length=32,
            max_length=34
        ),
        title: str = Form(..., description="Заголовок сообщения"),
        message: str = Form(..., description="Тело сообщения"),
        destination_user_id: int = Form(..., alias="destinationUserId", description="Id пользователя"),
        idinfo: int = Form(0, description="Id сообщения с файлами")
):
    bonch = BonchMessage(miden)
    message_raw = bonch.new(title=title, message=message, destination_user=destination_user_id, idinfo=idinfo)
    return ResponseBuilder().result(status=message_raw[0], info=message_raw[1], data=None)


@router.post(
    path="/answer",
    responses=DefaultErrors().errors,
    tags=["Сообщения"],
    summary="Ответить на сообщения"
)
async def answer_messages(
        miden: str = Header(
            ...,
            description="Токен для доступа к лк",
            alias="X-Token-Miden",
            min_length=32,
            max_length=34
        ),
        message: str = Form(..., description="Тело ответа"),
        destination_message_id: int = Form(
            ...,
            alias="destinationMessageId",
            description="Id сообщения на которое надо ответить"
        ),
        idinfo: int = Form(0, description="Id сообщения с файлами")
):

    bonch = BonchMessage(miden)
    message_raw = bonch.answer(message=message, destination_message=destination_message_id, idinfo=idinfo)
    return ResponseBuilder().result(status=message_raw[0], info=message_raw[1], data=None)


@router.get(
    path="/history",
    responses=MessageHistoryErrors().errors,
    tags=["Сообщения"],
    summary="История сообщения"
)
async def history_messages(
        miden: str = Header(
            ...,
            description="Токен для доступа к лк",
            alias="X-Token-Miden",
            min_length=32,
            max_length=34
        ),
        message_id: int = Form(
            ...,
            alias="messageId",
            description="Id сообщения"
        ),
):
    bonch = BonchMessage(miden)
    history_raw = bonch.history(message_id)
    if history_raw[0] == 200:
        return ResponseBuilder().result(status=history_raw[0], data=history_raw[1])
    else:
        return ResponseBuilder().result(status=history_raw[0], info=history_raw[1], data=None)

@router.get(
    path="/read",
    tags=["Сообщения"],
    summary="Прочитать сообщение",
    responses=MessagesErrors().errors,
)
async def read_message(
    miden: str = Header(
        ...,
        description="Токен для доступа к лк",
        alias="X-Token-Miden",
        min_length=32,
        max_length=34
    ),
    id: int = Query(
        ...,
        alias="messageId",
        description="Id сообщения"
    ),
):
    message = BonchMessage(miden).read(id=id)
    if message[0] == 200:
        return ResponseBuilder().result(data=message[1])
    else:
        return ResponseBuilder().result(data=None, status=message[0], info=message[1])
