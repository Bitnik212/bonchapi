from server.app.errors.ClientErrors.DefaultClientErrorModels import DefaultClientErrorModels
from server.core.models.HTTPErrors import HTTPErrors


class DefaultErrors(HTTPErrors):
    def __init__(self):
        super().__init__()
        self._client_errors = DefaultClientErrorModels()
