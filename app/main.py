import time
from contextlib import asynccontextmanager
import fastapi_cdn_host

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from prometheus_client import disable_created_metrics, generate_latest, make_asgi_app
from app.core.config import Settings
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core import logs
from app.db import test_engine_connectivity
from app.observability.metrics import HTTP_REQUESTS_TOTAL, Metrics_Basic_Auth_ASGIMiddleware
from app.routers import auth, management, pasted
from asgi_correlation_id import CorrelationIdMiddleware, correlation_id

from app.scripts import bootstrap

@asynccontextmanager
async def lifespan(app: FastAPI):
    # db.create_db_and_tables()
    logs.setup_logger()
    test_engine_connectivity()
    bootstrap.run()

    yield


def create_app():
    # Creating the setting object here so i can monkey patch the envs more easily.
    settings = Settings()

    app = FastAPI(
        lifespan=lifespan,
        root_path="/api",
        redoc_url= "/redoc" if settings.development else None,
        openapi_url="/openapi.json" if settings.development else None,
        docs_url="/docs" if settings.development else None,
    )

    if settings.Metrics_Enabled:
        disable_created_metrics()
        metrics_app = make_asgi_app()
        app.mount("/metrics", Metrics_Basic_Auth_ASGIMiddleware(
            metrics_app,
            settings.Metrics_Username,
            settings.Metrics_Password
        ))

    # This is beneficial during the Iran's internet distruptions. The OpenAPI front-end wasn't able to load on that shitty days.
    fastapi_cdn_host.patch_docs(app) 


    if not settings.development:
        app.frontend(path="/", directory="dist", fallback="index.html")

    app.include_router(auth.router)
    app.include_router(pasted.router)
    app.include_router(management.router)

    logger = logs.get_logger()

    ## Middlewares
    @app.middleware("http")
    async def log_process_time(request: Request, call_next):
        """It just logs the requests for the sake of keeping track of the general performance metrics"""

        start_time = time.perf_counter()
        response = None

        try:
            response = await call_next(request)
            return response
        finally:
            process_time = time.perf_counter() - start_time
            logger.debug(
                "request_completed",
                extra={
                    "tags": {
                        "http_method": request.method,
                        "path": request.url.path,
                        "process_time": round(process_time, 4),
                    },
                },
            )
            route = request.scope.get("route")
            route_path = route.path if route else request.url.path
            status_code = response.status_code if response else 500

            HTTP_REQUESTS_TOTAL.labels(
                method=request.method,
                route=route_path,
                status=status_code,
            ).inc()



    app.add_middleware(CorrelationIdMiddleware)


    ## Exception handlers

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, exc):
        logger.error(
            "http_exception",
            extra={
                "tags": {
                    "http_method": request.method,
                    "path": request.url.path,
                    "detail": repr(exc),
                    "status_code": exc.status_code,
                },
            },
        )
        return await http_exception_handler(request, exc)


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        status_code = 422

        logger.warning(
            "validation_error",
            extra={
                "tags": {
                    "http_method": request.method,
                    "path": request.url.path,
                    "detail": repr(exc),
                    "status_code": status_code,
                },
            },
        )

        if not settings.development:
            return JSONResponse(
                status_code=422,
                content=jsonable_encoder(
                    {"detail": "Invalid request. Please check the input and try again."}
                ),
            )

        return await request_validation_exception_handler(request, exc)


    return app


app = create_app()
