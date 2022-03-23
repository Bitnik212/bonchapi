from app.server.core.exceptions.ResponseException import ResponseException


class AppConfig:

    def __init__(self):
        self.debug: bool = False
        self.subclass_name: str = ""
        self.title: str = "Default app setup"
        self.description: str = ""
        self.version: str = "0.0.0"
        self.version_code: int = int(self.version[0:1])
        self.version_prefix: str = "/v"+str(self.version_code)
        self.mount_path: str = "/default"
        self.servers: list = [
                      {"url": "http://0.0.0.0:8000/v0", "description": "Development server. Version "+self.version},
                  ]
        self.root_path: str = ""
        self.openapi_prefix: str = ""
        self.exception_handlers: dict = {
                422: ResponseException.validation_error, # Не работает (((((
                404: ResponseException.not_found,
                501: ResponseException.not_impl,
            }


