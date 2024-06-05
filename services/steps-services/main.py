from fastapi import FastAPI

from app.api import router

app = FastAPI(openapi_url="/api/v1/steps/openapi.json", docs_url="/api/v1/steps/docs")

app.include_router(router, prefix='/api/v1/steps')
