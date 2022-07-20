import asyncio

from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Listing(BaseModel):
    lot_number: Union[int, None] = None
    make: Union[str, None] = None


listings = {
    "0": {"lot_number": 0, "make": "Porsche"},
    "1": {"lot_number": 0, "make": "Ferrari"},
}


@app.get("/")
async def root():
    return {"message": "Welcome to the car-auction-api!"}


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


async def foo(bar):
    print(f'{bar} started')
    await asyncio.sleep(1)
    print(f'{bar} finished')


async def main():
    await asyncio.gather(foo('first'), foo('second'))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
