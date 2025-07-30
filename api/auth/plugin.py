from fastapi import FastAPI
from api.plugin import Plugin
from api.auth.router import auth_router
from api.auth.user import user_router
from api.auth.access import access_router


class AuthPlugin(Plugin):
    def build(self, app: FastAPI) -> FastAPI:
        app.include_router(auth_router)
        app.include_router(user_router)
        app.include_router(access_router)
        return app
