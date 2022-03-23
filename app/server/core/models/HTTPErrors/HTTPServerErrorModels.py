from app.server.core.exceptions.HTTP.HTTPStatusClass import HTTPStatusClass
from app.server.core.models.HTTPErrors.StatusCode.HTTPError500Model import HTTPError500Model
from app.server.core.utils.HTTPErrorModelsIterator import HTTPErrorModelsIterator


class HTTPServerErrorModels(object):
    def __iter__(self):
        return HTTPErrorModelsIterator(self)

    @property
    def internal_server_error(self) -> HTTPStatusClass:
        """
        На сервере произошла критическая ошибка
        :return: HTTPStatusClass
        """
        error = HTTPStatusClass()
        error.code = 500
        error.description = "На сервере произошла критическая ошибка"
        error.model = HTTPError500Model
        return error

    # @property
    # def not_implemented(self) -> HTTPStatusClass:
    #     error = HTTPStatusClass()
    #     error.code = 501
    #     error.description = "Не сделан"
    #     return error

    @property
    def bad_gateway(self) -> HTTPStatusClass:
        error = HTTPStatusClass()
        error.code = 502
        error.description = "Ошибка доступа к серверу"
        return error

    @property
    def service_unavailable(self) -> HTTPStatusClass:
        error = HTTPStatusClass()
        error.code = 503
        return error

