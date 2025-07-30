from fastapi import FastAPI
import uvicorn

from . import __version__
from .auth.plugin import AuthPlugin
from .suspension.plugin import SuspensionPlugin
from .plugin import add_plugins
from dotenv import load_dotenv


def init_app() -> FastAPI:
    load_dotenv()

    app = FastAPI()

    add_plugins(app, [AuthPlugin(), SuspensionPlugin()])

    return app


app = init_app()


@app.get("/")
def root():
    return {"msg": f"Online Ordering v{__version__}"}


if __name__ == "__main__":
    uvicorn.run("api.__main__:app", port=5000, reload=True)
