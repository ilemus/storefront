from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel

from storefront.common.exceptions import DuplicateRecordException
from storefront.config import settings
from storefront.models.vendor import get_vendor_by_id, get_vendor_addresses, get_vendor_items


class CreateVendor(BaseModel):
    vendor_name: str


class AddAddress(BaseModel):
    street_address: str
    city: str
    zip_code: int
    state: str


class Item(BaseModel):
    item_name: str


NOT_CONNECTED = 'Not connected to database'
vendor_router = APIRouter()


@vendor_router.get("/vendor")
async def list_vendors(request: Request) -> JSONResponse:
    """
    Lists all vendors
    
    :param request:
    :param q: optional query string
    :param o: optional offset
    :param l: optional limit
    """
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        cursor.execute('SELECT * from vendor')
        results = cursor.fetchall()
        vendors = [{'id': result[0], 'name': result[1]} for result in results]
        cursor.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content={'vendors': vendors})
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@vendor_router.post("/vendor")
async def create_vendor(request: Request, vendor: CreateVendor) -> PlainTextResponse:
    """
    Lists all vendors
    
    :param request:
    :param vendor: object of vendor name
    """
    if settings.connect_to_database:
        # Add try catch for exceptions (duplicate name)
        try:
            cursor = request.state.sql_conn.cursor()
            cursor.execute('SELECT vendor_id FROM vendor WHERE vendor_name=%s', (vendor.vendor_name,))
            existing_vendor = cursor.fetchone()
            if existing_vendor is not None:
                raise DuplicateRecordException(f'A vendor with the name "{vendor.vendor_name}" already exists.')
            cursor.execute('INSERT INTO vendor (vendor_name) VALUES (%s)', (vendor.vendor_name,))
            cursor.close()
            request.state.sql_conn.commit()
            return PlainTextResponse(status_code=status.HTTP_201_CREATED, content="Successfully created.")
        except DuplicateRecordException as dre:
            return PlainTextResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(dre))
    return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@vendor_router.get("/vendor/{vendor_id}")
async def get_vendor(request: Request, vendor_id: int) -> JSONResponse:
    """
    Get vendor details
    
    :param request:
    :param vendor_id: vendor id
    """
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        vendor_name = get_vendor_by_id(cursor, vendor_id)
        addresses = get_vendor_addresses(cursor, vendor_id)
        items = get_vendor_items(cursor, vendor_id)
        cursor.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            'vendor_name': vendor_name,
            'addresses': addresses,
            'items': items
        })
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@vendor_router.delete("/vendor/{vendor_id}")
async def delete_vendor(request: Request, vendor_id: int) -> PlainTextResponse:
    """
    Get vendor details

    :param request:
    :param vendor_id: vendor id
    """
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        cursor.execute('DELETE FROM vendor WHERE vendor_id=%s', (vendor_id,))
        cursor.close()
        request.state.sql_conn.commit()
        return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content='Successfully deleted.')
    return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@vendor_router.post("/vendor/{vendor_id}/add-address")
async def add_address(request: Request, vendor_id: int, address: AddAddress) -> PlainTextResponse:
    if settings.connect_to_database:
        # TODO: add address already exists checks
        cursor = request.state.sql_conn.cursor()
        query = 'INSERT INTO vendor_address (vendor_id, street_address, city, zip_code, state)' \
                ' VALUES (%s, %s, %s, %s, %s)'
        values = (vendor_id, address.street_address, address.city, address.zip_code, address.state)
        cursor.execute(query, values)
        cursor.close()
        request.state.sql_conn.commit()
        return PlainTextResponse(status_code=status.HTTP_201_CREATED, content="Successfully added.")
    return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@vendor_router.post("/vendor/{vendor_id}/drop-address")
async def drop_address(request: Request, vendor_id: int, address: AddAddress) -> PlainTextResponse:
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        query = 'DELETE FROM vendor_address ' \
                'WHERE vendor_id=%s AND street_address=%s AND city=%s AND zip_code=%s AND state=%s)'
        values = (vendor_id, address.street_address, address.city, address.zip_code, address.state)
        cursor.execute(query, values)
        cursor.close()
        request.state.sql_conn.commit()
        return PlainTextResponse(status_code=status.HTTP_201_CREATED, content="Successfully dropped.")
    return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@vendor_router.post("/vendor/{vendor_id}/add-item")
async def add_item(request: Request, vendor_id: int, item: Item) -> PlainTextResponse:
    if settings.connect_to_database:
        # TODO: add item already exists checks
        cursor = request.state.sql_conn.cursor()
        query = 'INSERT INTO item (vendor_id, item_name)' \
                ' VALUES (%s, %s)'
        values = (vendor_id, item.item_name)
        cursor.execute(query, values)
        cursor.close()
        request.state.sql_conn.commit()
        return PlainTextResponse(status_code=status.HTTP_201_CREATED, content="Successfully added.")
    return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)


@vendor_router.post("/vendor/{vendor_id}/drop-item")
async def drop_item(request: Request, vendor_id: int, item: Item) -> PlainTextResponse:
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        query = 'DELETE FROM item ' \
                'WHERE vendor_id=%s AND item_name=%s)'
        values = (vendor_id, item.item_name)
        cursor.execute(query, values)
        cursor.close()
        request.state.sql_conn.commit()
        return PlainTextResponse(status_code=status.HTTP_201_CREATED, content="Successfully dropped.")
    return PlainTextResponse(status_code=status.HTTP_204_NO_CONTENT, content=NOT_CONNECTED)

# Item specific endpoints ??
# @vendor_router.post("/item")
