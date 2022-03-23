from app.server.core.exceptions.HTTP.HTTPStatusClass import HTTPStatusClass
from app.server.core.models.HTTPErrors.StatusCode.HTTPError422Model import HTTPError422Model
from app.server.core.utils.HTTPErrorModelsIterator import HTTPErrorModelsIterator


class HTTPClientErrorModels(object):
    def __iter__(self):
        return HTTPErrorModelsIterator(self)

    @property
    def bad_request(self) -> HTTPStatusClass:
        status = HTTPStatusClass()
        status.code = 400
        status.description = "Не правильный запрос"
        return status

    @property
    def forbidden(self) -> HTTPStatusClass:
        status = HTTPStatusClass()
        status.code = 403
        status.description = "Нет доступа"
        return status

    @property
    def not_found(self) -> HTTPStatusClass:
        status = HTTPStatusClass()
        status.code = 404
        status.description = "Не нашел"
        return status

    @property
    def method_not_allowed(self) -> HTTPStatusClass:
        status = HTTPStatusClass()
        status.code = 405
        status.description = "Метод не доступен"
        return status

    @property
    def validation_error(self) -> HTTPStatusClass:
        status = HTTPStatusClass()
        status.code = 422
        status.description = "Ошибка валидации данных"
        status.model = HTTPError422Model
        return status
