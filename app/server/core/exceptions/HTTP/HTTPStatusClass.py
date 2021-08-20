from server.core.models.DefaultResponseModel import DefaultResponseModel


class HTTPStatusClass:
    code: int
    model: DefaultResponseModel = DefaultResponseModel
    description: str = ""
