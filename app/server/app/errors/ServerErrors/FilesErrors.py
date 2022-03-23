from server.app.errors.ClientErrors.FilesClientErrorModels import FilesClientErrorModels
from server.core.models.HTTPErrors import HTTPErrors


class FilesErrors(HTTPErrors):

    def __init__(self):
        super().__init__()
        self._client_errors = FilesClientErrorModels()


