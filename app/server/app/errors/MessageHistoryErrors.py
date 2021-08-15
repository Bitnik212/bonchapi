from server.app.errors.ClientErrors.MessageHistoryClientErrorModels import MessageHistoryClientErrorModels
from server.core.models.HTTPErrors import HTTPErrors


class MessageHistoryErrors(HTTPErrors):
    def __init__(self):
        super().__init__()
        self._client_errors = MessageHistoryClientErrorModels()
