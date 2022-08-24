import asyncio
import json
import time
from typing import Union

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette_context import context, request_cycle_context

from src.context import ContextHandle


async def my_context_dependency(x_request_id=Header(...)):
    # When used a Depends(), this fucntion get the `X-Client_ID` header,
    # which will be documented as a required header by FastAPI.
    # use `x_client_id: str = Header(None)` for an optional header.
    print("x_request_id", x_request_id, "\n\n\n\n\n\n\n\nHEREHEREHERE")
    data = {"x_request_id": x_request_id}
    with request_cycle_context(data):
        # yield allows it to pass along to the rest of the request
        yield


# use it as Depends across the whole FastAPI app
app = FastAPI()  # dependencies=[Depends(my_context_dependency)])


@app.get("/")
async def hello():
    # client = context["x_client_id"]
    # return f"hello {client}"
    return {"msg": "Hello World"}


class Listing(BaseModel):
    lot_number: Union[int, None] = None
    make: Union[str, None] = None


listings = {
    "0": {"lot_number": 0, "make": "Porsche"},
    "1": {"lot_number": 0, "make": "Ferrari"},
}


@app.get("/listings/{listing_id}", response_model=Listing)
async def read_listing(listing_id: str):
    return listings[listing_id]


@app.put("/listings/{listing_id}, response_model=Listing")
async def update_listing(listing_id: str, listing: Listing):
    update_item_encoded = jsonable_encoder(listing)
    listings[listing_id] = update_item_encoded
    return update_item_encoded


@app.post("/listings/")
async def create_listing(listing: Listing):
    return listing


"""
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
"""


@app.middleware("http")
async def add_request_context(request: Request, call_next):
    response = await call_next(request)
    x_request_id = request.headers["x-request_id"]
    data = {"X-Request-ID": x_request_id}
    response.headers["X-Context"] = json.dumps(data)
    return response
