import asyncio
import sqlite3

from fastapi import FastAPI, Request


def create_app():
    app = FastAPI()
    conn = sqlite3.connect('search.db')

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        request.state.sql_conn = conn
        response = await call_next(request)
        return response

    @app.on_event("startup")
    async def startup():
        await db.create_pool()

    @app.get("/s")
    async def search(request: Request, q: str = '', s: int = 0, l: int = 0):
        """
        Here is all the functionality.
        This can be profitable; consider offering higher search results for select phrases;
        For search keys (list of 5) put $10 * x down per month. The highest bidder gets the first match, second highest next, then regular search.
        Store popularity of search result.
        Second DB for managing expiration of such search prefernces and auditable.
        
        :param request:
        :param q: query string
        :param s: skip
        :param l: limit
        """
        if q == '':
            return {}
        cursor = request.state.sql_conn.cursor()
        # sort by best results first
        query_str = f"select v from t where k=:q"
        cursor.execute(query_str, {"q": q})
        results = cursor.fetchall()
        return {'r': results}

    return app

app = create_app()
