from fastapi import FastAPI
from api.plugin import Plugin
from api.suspension.router import suspension_router


class SuspensionPlugin(Plugin):
    def build(self, app: FastAPI) -> FastAPI:
        app.include_router(suspension_router)
        return app
