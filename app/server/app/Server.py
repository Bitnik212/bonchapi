from enum import Enum

from app.server.app.routes import ServerRoutes
from app.server.core.App import App
from app.server.core.AppConfig import AppConfig


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
            {"url": "http://localhost:8000/", "description": "Development server"},
        ]
        return app


