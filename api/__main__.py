from fastapi import FastAPI
import uvicorn
from . import __version__
from .auth.router import auth_router
from .auth.user import user_router
from .auth.access import access_router
from dotenv import load_dotenv


def init_app() -> FastAPI:
    load_dotenv()

    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(access_router)

    return app


app = init_app()


@app.get("/")
def root():
    return {"msg": f"Online Ordering v{__version__}"}


if __name__ == "__main__":
    uvicorn.run("api.__main__:app", port=5000, reload=True)
