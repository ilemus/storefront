from datetime import datetime

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel

from storefront.common.exceptions import DuplicateRecordException
from storefront.config import settings
from storefront.models.person import get_person_by_id

"""
person_id INT NOT NULL AUTO_INCREMENT, '
'person_first_name VARCHAR(18), '
'person_last_name VARCHAR(18),
'person_email VARCHAR(64), '
"""


class Person(BaseModel):
    person_first_name: str
    person_last_name: str
    person_email: str


class Address(BaseModel):
    street_address: str
    city: str
    zip_code: int
    state: str


NOT_CONNECTED = 'Not connected to database'
person_router = APIRouter()


@person_router.get("/person")
async def list_people(request: Request) -> JSONResponse:
    """
    Lists all people

    :param request:
    """
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        cursor.execute('SELECT person_id, person_first_name, person_last_name, person_email FROM person')
        results = cursor.fetchall()
        people = [{'id': result[0], 'first_name': result[1], 'last_name': result[2], 'email': result[3]}
                  for result in results]
        cursor.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content={'people': people})
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@person_router.post("/person")
async def create_person(request: Request, person: Person) -> PlainTextResponse:
    """
    Create a new person.

    :param request:
    :param person: object of person info
    """
    if settings.connect_to_database:
        # Add try catch for exceptions (duplicate name)
        try:
            cursor = request.state.sql_conn.cursor()
            query = 'SELECT person_id FROM person ' \
                    'WHERE person_first_name=%s AND person_last_name=%s AND person_email=%s'
            values = (person.person_first_name, person.person_last_name, person.person_email)
            cursor.execute(query, values)
            existing_person = cursor.fetchone()
            if existing_person is not None:
                raise DuplicateRecordException(f'A person with the name '
                                               f'"{person.person_first_name} {person.person_last_name}" already exists '
                                               f'with email {person.person_email}.')
            query = 'INSERT INTO person (person_first_name, person_last_name, person_email, created_date) ' \
                    'VALUES (%s, %s, %s, %s)'
            values = (person.person_first_name, person.person_last_name, person.person_email, datetime.utcnow())
            cursor.execute(query, values)
            cursor.close()
            request.state.sql_conn.commit()
            return PlainTextResponse(status_code=status.HTTP_201_CREATED, content="Successfully created.")
        except DuplicateRecordException as dre:
            return PlainTextResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(dre))
    return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@person_router.get("/person/{person_id}")
async def get_person(request: Request, person_id: int) -> JSONResponse:
    """
    Get person details

    :param request:
    :param person_id: person id
    """
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        # need to update by creating model
        person_info = get_person_by_id(cursor, person_id)
        addresses = get_person_by_id(cursor, person_id)
        cursor.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            **person_info,
            'addresses': addresses
        })
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@person_router.delete("/person/{person_id}")
async def delete_person(request: Request, person_id: int) -> PlainTextResponse:
    """
    Delete person

    :param request:
    :param person_id: person id
    """
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        cursor.execute('DELETE FROM person WHERE person_id=%s', (person_id,))
        cursor.close()
        request.state.sql_conn.commit()
        return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content='Successfully deleted.')
    return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@person_router.post("/person/{person_id}/add-address")
async def add_address(request: Request, person_id: int, address: Address) -> PlainTextResponse:
    if settings.connect_to_database:
        # TODO: add address already exists checks
        cursor = request.state.sql_conn.cursor()
        query = 'INSERT INTO person_address (person_id, street_address, city, zip_code, state)' \
                ' VALUES (%s, %s, %s, %s, %s)'
        values = (person_id, address.street_address, address.city, address.zip_code, address.state)
        cursor.execute(query, values)
        cursor.close()
        request.state.sql_conn.commit()
        return PlainTextResponse(status_code=status.HTTP_201_CREATED, content="Successfully added.")
    return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@person_router.post("/person/{person_id}/drop-address")
async def drop_address(request: Request, person_id: int, address: Address) -> PlainTextResponse:
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        query = 'DELETE FROM person_address ' \
                'WHERE person_id=%s AND street_address=%s AND city=%s AND zip_code=%s AND state=%s)'
        values = (person_id, address.street_address, address.city, address.zip_code, address.state)
        cursor.execute(query, values)
        cursor.close()
        request.state.sql_conn.commit()
        return PlainTextResponse(status_code=status.HTTP_201_CREATED, content="Successfully dropped.")
    return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


# Order specific endpoints ??
# @person_router.post("/order")
