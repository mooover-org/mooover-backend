from fastapi import FastAPI

from app.api import router

app = FastAPI(openapi_url="/api/v1/auth/openapi.json", docs_url="/api/v1/auth/docs")

app.include_router(router, prefix='/api/v1/auth')
