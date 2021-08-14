from enum import Enum

from server.app.routes import SignInRoutes


class ServerRoutes(Enum):
    signIn = SignInRoutes.router

