from fastapi import FastAPI
import uvicorn
from . import __version__


def init_app() -> FastAPI:
    app = FastAPI()
    return app


app = init_app()


@app.get("/")
def root():
    return {"msg": f"Online Ordering v{__version__}"}


if __name__ == "__main__":
    uvicorn.run("__main__:app", port=5000, reload=True)
