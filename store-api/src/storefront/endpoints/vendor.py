from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from storefront.config import settings


class CreateVendor(BaseModel):
    vendor_name: str


vendor_router = APIRouter()

@vendor_router.get("/vendor")
async def list_vendors(request: Request, q: str = '', o: int = 0, l: int = 0) -> JSONResponse:
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
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='Not connected to database')

@vendor_router.post("/vendor")
async def create_vendor(request: Request, vendor: CreateVendor) -> JSONResponse:
    """
    Lists all vendors
    
    :param request:
    :param q: optional query string
    :param o: optional offset
    :param l: optional limit
    """
    if settings.connect_to_database:
        # Add try catch for exceptions (duplicate name)
        cursor = request.state.sql_conn.cursor()
        cursor.execute('INSERT INTO vendor ("%s")', (vendor.vendor_name,))
        result = cursor.fetchone()
        cursor.close()
        request.state.sql_conn.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='Not connected to database')

@vendor_router.get("/vendor/{vendor_id}")
async def get_vendor(request: Request, vendor_id: int) -> JSONResponse:
    """
    Lists all vendors
    
    :param request:
    :param q: optional query string
    :param o: optional offset
    :param l: optional limit
    """
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        cursor.execute('SELECT vendor_name from vendor where vendor_id=%s', (vendor_id,))
        result = cursor.fetchone()
        cursor.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content={'vendor_name': str(result[0])})
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='Not connected to database')

