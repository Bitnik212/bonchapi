from app.server.core.models.HTTPErrors.HTTPClientErrorModels import HTTPClientErrorModels
from app.server.core.models.HTTPErrors.HTTPServerErrorModels import HTTPServerErrorModels


class HTTPErrors:
    def __init__(self):
        self._server_errors = HTTPServerErrorModels()
        self._client_errors = HTTPClientErrorModels()

    @property
    def errors(self):
        errors = {}
        for error in self._server_errors:
            errors.update({
                error.code: {"model": error.model, "description": error.description}
            })
        for error in self._client_errors:
            errors.update({
                error.code: {"model": error.model, "description": error.description}
            })
        return errors
