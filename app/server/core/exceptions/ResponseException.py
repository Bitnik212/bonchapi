from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi import Request, status
from starlette.responses import JSONResponse
from app.server.core.utils.ResponseBuilder import ResponseBuilder


class ResponseException:

    def not_found(self, r: Request, e: HTTPException) -> JSONResponse:
        return ResponseBuilder().not_found()

    def not_impl(self, r: Request, e: HTTPException) -> JSONResponse:
        return ResponseBuilder().not_impl()

    def handle(self, r: Request, e: HTTPException) -> JSONResponse:
        try:
            data = dict(e.args)
        except:
            data = r.body()
        return ResponseBuilder().result(info=str(e.detail), data=data, status=e.status_code)
        # return JSONResponse(status_code=500, content=e.detail)

    def validation_error(self, r: Request, e: RequestValidationError) -> JSONResponse:
        """

        :param r:
        :param e:
        :return:
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
