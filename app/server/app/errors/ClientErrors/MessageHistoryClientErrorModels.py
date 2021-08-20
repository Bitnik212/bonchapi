from server.app.errors.models.MessageHistoryHTTPStatus200Model import MessageHistoryHTTPStatus200Model
from server.core.exceptions.HTTP.HTTPStatusClass import HTTPStatusClass
from server.core.models.HTTPErrors import HTTPClientErrorModels


class MessageHistoryClientErrorModels(HTTPClientErrorModels):

    @property
    def success(self) -> HTTPStatusClass:
        status = HTTPStatusClass()
        status.code = 200
        status.model = MessageHistoryHTTPStatus200Model
        return status
