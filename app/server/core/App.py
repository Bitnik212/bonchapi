import typing

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from server.core.exceptions.ResponseException import ResponseException
from server.core.AppConfig import AppConfig
from server.core.AppRoutes import AppRoutes


class App:

    def __init__(self):
        self.config: AppConfig or None = None
        self.routes: AppRoutes or None = None
        # self.now_version: SubAppVersion or None = None
        self.__middlewares = [[]]

    def _instance(self) -> FastAPI:
        if self.config is None:
            config = AppConfig()
        else:
            config = self.config
        app = FastAPI(
            title=config.title,
            version=config.version,
            openapi_prefix=config.openapi_prefix,
            description=config.description,
            debug=config.debug,
            servers=config.servers,
            root_path=config.root_path,
            exception_handlers=config.exception_handlers
        )
        # add middlewares
        if self.__middlewares:
            for middleware in self.__middlewares:
                if middleware:
                    app.add_middleware(middleware_class=middleware[0])
                    if middleware[1]:
                        app.add_middleware(middleware_class=middleware[0], options=middleware[1:])
        self.add_validation_exception_handler(app)  # fix прикола fastapi
        # add all routes in app
        if self.routes:
            for router in self.routes:
                if router:
                    app.include_router(router.value)
        return app

    def get_instance(self) -> FastAPI:
        return self._instance()

    @staticmethod
    def add_validation_exception_handler(app: FastAPI):
        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(r: Request, e: RequestValidationError):
            return ResponseException.validation_error(r, e)

    # def _configure(self) -> AppConfig:
    #     """
    #     Сделать свою конфигурацию подприлжения(App)
    #
    #     :return: AppConfig
    #     """
    #     app = AppConfig()
    #     app.title = "Default docs"
    #     app.mount_path = "/"
    #     return app

    def add_middleware(self, middleware: type, **options: typing.Any):
        self.__middlewares.append([middleware, options])
