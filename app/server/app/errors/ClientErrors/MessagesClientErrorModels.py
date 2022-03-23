from server.app.errors.models.MessagesHTTPStatus200Model import MessagesHTTPStatus200Model
from server.core.exceptions.HTTP.HTTPStatusClass import HTTPStatusClass
from server.core.models.HTTPErrors import HTTPClientErrorModels


class MessagesClientErrorModels(HTTPClientErrorModels):

    @property
    def success(self) -> HTTPStatusClass:
        status = HTTPStatusClass()
        status.code = 200
        status.model = MessagesHTTPStatus200Model
        return status
