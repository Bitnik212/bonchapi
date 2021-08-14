from server.app.errors.ClientErrors.SignInClientErrorModels import SignInClientErrorModels
from server.core.models.HTTPErrors import HTTPErrors


class SignInErrors(HTTPErrors):

    def __init__(self):
        super().__init__()
        self._client_errors = SignInClientErrorModels()
