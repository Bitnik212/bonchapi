from enum import Enum

from fastapi import APIRouter

from server.app.routes import SignInRoutes, MessagesRoutes, FileRoutes, ScheduleRoutes


class ServerRoutes(Enum):
    signIn: APIRouter = SignInRoutes.router
    messages: APIRouter = MessagesRoutes.router
    files: APIRouter = FileRoutes.router
    schedule: APIRouter = ScheduleRoutes.router

