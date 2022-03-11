from fastapi import FastAPI

from app.api import router

app = FastAPI(openapi_url="/api/v1/users/openapi.json", docs_url="/api/v1/users/docs")

app.include_router(router, prefix='/api/v1/users', tags=['users'])
