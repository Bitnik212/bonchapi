from server.app.errors.ClientErrors.MessagesClientErrorModels import MessagesClientErrorModels
from server.core.models.HTTPErrors import HTTPErrors


class MessagesErrors(HTTPErrors):
    def __init__(self):
        super().__init__()
        self._client_errors = MessagesClientErrorModels()
