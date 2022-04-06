import asyncio
import mysql.connector

from fastapi import FastAPI, Request
from storefront.endpoints.search import search_router
from storefront.config import settings

def create_app():
    app = FastAPI(title="Storefront API", openapi_url="/openapi.json")
    if settings.connect_to_database:
        conn = mysql.connector.connect(user='webapp', password='webbapp_secret_password',
                                    host='adminer',
                                    port=8080,
                                    database='storefront')
    app.include_router(search_router, prefix="/api/v1")

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        if settings.connect_to_database:
            request.state.sql_conn = conn
        response = await call_next(request)
        return response

    @app.on_event("shutdown")
    async def shutdown():
        # cleanup
        if settings.connect_to_database:
            conn.close()

    return app

app = create_app()
