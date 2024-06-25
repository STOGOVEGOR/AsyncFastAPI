import asyncio
from collections import OrderedDict
from typing import List, Union

from fastapi import FastAPI
from sqlalchemy.future import select
from sqlalchemy import text
from sqlalchemy.sql import Select

# # Uncomment this for run test
# from api_async.database import async_session, engine
# from api_async.models import Data1, Data2, Data3

# # Comment this out for run test
from database import async_session, engine
from models import Data1, Data2, Data3


app = FastAPI()


async def fetch_data(query: Union[str, Select]) -> List:
    async with async_session() as db:
        try:
            if isinstance(query, str):
                result = await db.execute(text(query))
                data = result.fetchall()
            else:
                result = await db.execute(query)
                data = result.scalars().all()
            return data
        except asyncio.TimeoutError:
            return []  # empty list as indicator
        except Exception as e:
            return []  # empty list as indicator


@app.get("/", tags=["Root"])
async def welcome():
    return "Here we are..."


@app.get("/data")
async def get_data():
    tasks = [
        fetch_data("SELECT * FROM data_1 WHERE id BETWEEN 1 AND 10"),
        fetch_data("SELECT * FROM data_1 WHERE id BETWEEN 31 AND 40"),
        fetch_data(select(Data2).filter(Data2.id.between(11, 20))),
        fetch_data(select(Data2).filter(Data2.id.between(41, 50))),
        fetch_data(select(Data3).filter(Data3.id.between(21, 30))),
        fetch_data(select(Data3).filter(Data3.id.between(51, 60))),
    ]

    results = []
    try:
        gathered_results = await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=2.0)
        results.extend(gathered_results)
    except asyncio.TimeoutError:
        results = [asyncio.TimeoutError() for _ in range(len(tasks))]

    # handling errors and retry requests
    for idx, result in enumerate(results):
        if isinstance(result, Exception):
            try:
                result = await tasks[idx]
                results[idx] = result
            except Exception as e:
                results[idx] = []  # empty list as indicator

    combined_data = [item for sublist in results for item in sublist if not isinstance(sublist, Exception)]
    sorted_data = sorted(combined_data, key=lambda x: x.id)

    ordered_data = [
        OrderedDict([('id', item.id), ('name', item.name)])
        for item in sorted_data
    ]

    return ordered_data


@app.get("/check_connection")
async def check_db_connection():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.fetchone()
            if row and row[0] == 1:
                return {"status": "Connected to the database"}
            else:
                return {"status": "Failed to connect to the database: Invalid response from database"}
    except Exception as e:
        return {"status": f"Failed to connect to the database: {e}"}
