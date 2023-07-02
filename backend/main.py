from backend.container import Container


from backend import endpoints
from fastapi import FastAPI
import os


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[endpoints])
    app = FastAPI(root_path=os.getenv("ROOT_PATH", ""))
    app.container = container
    app.include_router(endpoints.rest_v1_router)
    return app


app = create_app()
app.include_router(endpoints.rest_v1_router)
