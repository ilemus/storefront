import asyncio
import logging
import mysql.connector
import sys

from fastapi import FastAPI, Request
from storefront.endpoints.search import search_router
from storefront.config import settings
from storefront.tables import TABLES

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)


def update_tables(conn):
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES;')
    table_results = cursor.fetchall()
    table_names = set()
    for table in table_results:
        table_names.add(table[0])
    changes = False
    for key in TABLES.keys():
        if key not in table_names:
            cursor.execute(TABLES.get(key))
            logger.info(f"Successfully create {key}")
            changes = True
    if changes:
        conn.commit()
        logger.info('Created missing tables')
    cursor.close()


def create_app():
    app = FastAPI(title="Storefront API", openapi_url="/openapi.json")
    if settings.connect_to_database:
        logger.info('connecting to database')
        conn = mysql.connector.connect(user=settings.mysql.username, password=settings.mysql.password,
                                        host=settings.mysql.hostname, port=settings.mysql.port,
                                        database=settings.mysql.database, connect_timeout=5)
        logger.info('connected to database!')
        update_tables(conn)
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
