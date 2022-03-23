from enum import Enum

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi import Request, status
from starlette.responses import JSONResponse
from app.server.core.utils.ResponseBuilder import ResponseBuilder


class ResponseException(Enum):

    @staticmethod
    def not_found(r: Request, e: HTTPException) -> JSONResponse:
        return ResponseBuilder().not_found()

    @staticmethod
    def not_impl(r: Request, e: HTTPException) -> JSONResponse:
        return ResponseBuilder().not_impl()

    @staticmethod
    def handle(r: Request, e: HTTPException) -> JSONResponse:
        try:
            data = dict(e.args)
        except:
            data = r.body()
        return ResponseBuilder().result(info=str(e.detail), data=data, status=e.status_code)

    @staticmethod
    def validation_error(r: Request, e: RequestValidationError) -> JSONResponse:
        """

        """
        try:
            loc = str(e.args[0][0]).split("loc")[1].replace("=", '').replace("(", '').replace(")", "").replace("'", '').replace(" ", "").split(",")
            info = str(e.args[0][0].exc)
            data = {
                "body": e.body,
                "validation": {
                    "info": str(e.args[0][0].exc),
                    "in": loc[0],
                    "inParam": loc[1]
                }
            }
        except:
            data = {}
            info = "Ошибка обработки валидатора"
        return ResponseBuilder().result(info=info, data=data, status=422)
