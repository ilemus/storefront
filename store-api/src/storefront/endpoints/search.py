from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from storefront.config import settings

search_router = APIRouter()

@search_router.get("/s")
async def search(request: Request, q: str = '', o: int = 0, l: int = 0) -> JSONResponse:
    """
    Here is all the functionality.
    This can be profitable; consider offering higher search results for select phrases;
    For search keys (list of 5) put $10 * x down per month. The highest bidder gets the first match, second highest next, then regular search.
    Store popularity of search result.
    Second DB for managing expiration of such search prefernces and auditable.
    
    :param request:
    :param q: query string
    :param o: offset
    :param l: limit
    """
    if q == '':
        return {}
    
    if settings.connect_to_database:
        cursor = request.state.sql_conn.cursor()
        # sort by best results first
        query_str = f"select v from s where k=%s"
        cursor.execute(query_str, (q,))
        results = cursor.fetchall()
        return JSONResponse(status_code=status.HTTP_200_OK, content={'r': results})
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="No connection to database")
