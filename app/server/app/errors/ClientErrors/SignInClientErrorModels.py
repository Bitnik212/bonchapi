from server.app.errors.models.SignInHTTPStatus200Model import SignInHTTPStatus200Model
from server.core.exceptions.HTTP.HTTPStatusClass import HTTPStatusClass
from server.core.models.HTTPErrors import HTTPClientErrorModels


class SignInClientErrorModels(HTTPClientErrorModels):

    @property
    def success(self) -> HTTPStatusClass:
        status = HTTPStatusClass()
        status.code = 200
        status.model = SignInHTTPStatus200Model
        return status


