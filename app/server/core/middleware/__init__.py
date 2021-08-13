from starlette.types import ASGIApp, Scope, Receive, Send


class AppMiddleware:

    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.exclude_list = ["/docs", "/openapi.json", "/"]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.app(scope, receive, send)