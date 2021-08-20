from enum import Enum

from server.app.routes import ServerRoutes
from server.core.App import App
from server.core.AppConfig import AppConfig


class Server(App):

    def __init__(self):
        super().__init__()
        self.routes: id(Enum) = ServerRoutes
        self.config = self._configure()
        self.debug: bool = False

    @staticmethod
    def _configure() -> AppConfig:
        app = AppConfig()
        app.title = "Bonch RestAPI"
        app.version = "0.0.1"
        app.mount_path = "/"
        app.servers = [
            {"url": "http://127.0.0.1:8000/", "description": "Development server"},
        ]
        return app


