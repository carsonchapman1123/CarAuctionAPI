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


@app.get("/porsche")
async def porsche():
    return {"message": "Porsche cars"}


@app.get("/listing")
async def listing():
    return {"essentials": {"seller": "Carson", "Location": "San Jose, CA"}}


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
