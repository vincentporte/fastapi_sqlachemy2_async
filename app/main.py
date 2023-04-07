from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.services.database import sessionmanager
from app.users.routes import router as user_router


class MainApp:
    def __init__(self, init_db=True):
        lifespan = None

        if init_db:
            sessionmanager.init(settings.DATABASE_URL)

            @asynccontextmanager
            async def lifespan(app: FastAPI):
                yield
                if sessionmanager._engine is not None:
                    await sessionmanager.close()

        self.app = FastAPI(title="FastAPI server", lifespan=lifespan)
        self.add_static_files()
        self.add_routes()
        self.add_middleware()
        self.custom_openapi()

    def add_static_files(self):
        self.app.mount("/static", StaticFiles(directory="app/static"), name="static")

    def add_routes(self):
        @self.app.get("/api/status")
        async def status():
            return {"status": "up"}

        self.app.include_router(user_router, prefix="/api", tags=["user"])

    def add_middleware(self):
        # CORS
        origins = ["http://localhost", "http://localhost:8080", "https://benevoles.rencontrerlarche.com"]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # custom middleware that adds an "X-Process-Time" header to the response,
        # indicating that the processing time for the request was fast
        @self.app.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            response = await call_next(request)
            response.headers["X-Process-Time"] = "fast"
            return response

    def custom_openapi(self):
        if self.app.openapi_schema:
            return self.app.openapi_schema

        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version=settings.PROJECT_VERSION,
            description=settings.PROJECT_DESCRIPTION,
            routes=self.app.routes,
        )

        openapi_schema["info"]["x-logo"] = {"url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"}
        self.app.openapi_schema = openapi_schema


app = MainApp().app
