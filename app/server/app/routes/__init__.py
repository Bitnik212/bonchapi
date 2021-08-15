from enum import Enum

from server.app.routes import SignInRoutes, MessagesRoutes, FileRoutes


class ServerRoutes(Enum):
    signIn = SignInRoutes.router
    messages = MessagesRoutes.router
    files = FileRoutes.router

