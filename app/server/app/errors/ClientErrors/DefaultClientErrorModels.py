from server.core.exceptions.HTTP.HTTPStatusClass import HTTPStatusClass
from server.core.models.DefaultResponseModel import DefaultResponseModel
from server.core.models.HTTPErrors import HTTPClientErrorModels


class DefaultClientErrorModels(HTTPClientErrorModels):

    @property
    def success(self) -> HTTPStatusClass:
        status = HTTPStatusClass()
        status.code = 200
        status.model = DefaultResponseModel
        return status
