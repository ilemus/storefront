import asyncio
import logging
import mysql.connector
import os
import sys

from fastapi import FastAPI, Request
from storefront.endpoints.search import search_router
from storefront.config import settings

logger = logging.getLogger(__name__)

def create_app():
    logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.DEBUG, stream=sys.stdout)
    app = FastAPI(title="Storefront API", openapi_url="/openapi.json")
    if settings.connect_to_database:
        logger.info('connecting to database')
        logger.info(f'user={settings.mysql.username} password={settings.mysql.password} host={settings.mysql.hostname} port={settings.mysql.port} database={settings.mysql.database}')
        conn = mysql.connector.MySQLConnection(user=settings.mysql.username, password=settings.mysql.password,
                                    host=settings.mysql.hostname, port=settings.mysql.port,
                                    database=settings.mysql.database)
        logger.info('connected to database!')
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
