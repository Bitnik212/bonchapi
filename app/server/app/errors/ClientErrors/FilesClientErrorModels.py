from server.app.errors.models.FilesHTTPStatus200Model import FilesHTTPStatus200Model
from server.core.exceptions.HTTP.HTTPStatusClass import HTTPStatusClass
from server.core.models.HTTPErrors import HTTPClientErrorModels


class FilesClientErrorModels(HTTPClientErrorModels):

    @property
    def success(self) -> HTTPStatusClass:
        status = HTTPStatusClass()
        status.code = 200
        status.model = FilesHTTPStatus200Model
        return status

