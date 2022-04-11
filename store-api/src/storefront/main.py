import asyncio
import logging
import mysql.connector
import sys

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from storefront.endpoints.search import search_router
from storefront.endpoints.vendor import vendor_router
from storefront.config import settings
from storefront.tables import PARENT_TABLES, CHILDREN_TABLES, GRAND_CHILDREN_TABLES

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)


def _create_tables(cursor, existing_table_names: set, schema: dict) -> bool:
    changes = False
    for key in schema.keys():
        if key not in existing_table_names:
            try:
                cursor.execute(schema.get(key))
                logger.info(f"Successfully created {key}")
                changes = True
            except mysql.connector.errors.ProgrammingError as pe:
                logger.error(f'Failed to create {key} due to programming error: {str(pe)}')
            except mysql.connector.errors.DatabaseError as de:
                logger.error(f'Failed to create {key} due to DB error: {str(de)}')
    return changes


def _drop_all_tables(cursor):
    """
    WARNING DROPS ALL TABLES AND ALL DATA
    Don't know if this works or not
    :param cursor:
    :return:
    """
    unset_fk_checks = 'SET FOREIGN_KEY_CHECKS = 0'
    query = "SELECT concat('DROP TABLE IF EXISTS `', table_name, '`;') " \
            f"FROM information_schema.TABLES WHERE table_schema = '{settings.mysql.database}'"
    set_fk_checks = 'SET FOREIGN_KEY_CHECKS = 1'
    cursor.execute(unset_fk_checks)
    cursor.execute(query)
    cursor.execute(set_fk_checks)


def _drop_tables(cursor, existing_table_names: set, schema: dict) -> bool:
    changes = False
    for key in schema.keys():
        if key in existing_table_names:
            try:
                cursor.execute(f'DROP TABLE {key}')
                logger.info(f"Successfully dropped {key}")
                changes = True
            except mysql.connector.errors.ProgrammingError as pe:
                logger.error(f'Failed to create {key} due to programming error: {str(pe)}')
            except mysql.connector.errors.DatabaseError as de:
                logger.error(f'Failed to create {key} due to DB error: {str(de)}')
    return changes


def update_tables(conn) -> None:
    """
    Only do this in non-production. Drops and creates all tables.

    :param conn: connection to database
    :return:
    """
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES;')
    table_results = cursor.fetchall()
    table_names = set()
    for table in table_results:
        table_names.add(table[0])
    changes = False

    # Drop tables from lowest to highest
    changes = _drop_tables(cursor, table_names, GRAND_CHILDREN_TABLES) or changes
    changes = _drop_tables(cursor, table_names, CHILDREN_TABLES) or changes
    changes = _drop_tables(cursor, table_names, PARENT_TABLES) or changes
    if changes:
        conn.commit()
        logger.info('Dropped existing tables')
    changes = False

    table_names.clear()
    # Create tables from highest to lowest
    changes = _create_tables(cursor, table_names, PARENT_TABLES) or changes
    changes = _create_tables(cursor, table_names, CHILDREN_TABLES) or changes
    changes = _create_tables(cursor, table_names, GRAND_CHILDREN_TABLES) or changes
    if changes:
        conn.commit()
        logger.info('Created missing tables')
    cursor.close()


def create_app():
    _app = FastAPI(title="Storefront API", openapi_url="/openapi.json")
    if settings.connect_to_database:
        logger.info('connecting to database')
        conn = mysql.connector.connect(user=settings.mysql.username, password=settings.mysql.password,
                                       host=settings.mysql.hostname, port=settings.mysql.port,
                                       database=settings.mysql.database, connect_timeout=5)
        logger.info('connected to database!')
        update_tables(conn)
    _app.include_router(search_router, prefix='/api/v1')
    _app.include_router(vendor_router, prefix='/api/v1')

    @_app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        if settings.connect_to_database:
            request.state.sql_conn = conn
        response = await call_next(request)
        return response

    @_app.on_event("shutdown")
    async def shutdown():
        # cleanup
        if settings.connect_to_database:
            conn.close()

    return _app


app = create_app()
