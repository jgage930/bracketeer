from abc import ABC, abstractmethod
from fastapi import FastAPI


class Plugin(ABC):
    @abstractmethod
    def build(self, app: FastAPI) -> FastAPI: ...


def add_plugins(app: FastAPI, plugins: list[Plugin]) -> FastAPI:
    for plugin in plugins:
        app = plugin.build(app)

    return app
