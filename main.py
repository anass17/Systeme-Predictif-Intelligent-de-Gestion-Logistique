import random
from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()


types_list = ["DEBIT", "PAYMENT", "TRANSFER", "CASH"]
modes_list = ["Standard Class", "First Class", "Second Class", "Same Day"]
categories_list = ["Consumer Electronics", "Women's Clothing", "Golf Balls", "Trade-In", "Tennis & Racquet", "As Seen on  TV!", "Fishing", "CDs", "Garden", "Pet Supplies", "Cleats", "Boxing & MMA", "Baby", "Sporting Goods", "Hunting & Shooting", "Baseball & Softball", "Men's Footwear", "Basketball", "Girls' Apparel", "Strength Training", "Women's Apparel", "Camping & Hiking", "Fitness Accessories", "DVDs", "Hockey", "Electronics", "Crafts", "Men's Clothing", "Lacrosse", "Books", "Health and Beauty", "Music", "Video Games", "Shop By Sport", "Cardio Equipment", "Kids' Golf Clubs", "Cameras", "Soccer", "Accessories", "Children's Clothing", "Golf Gloves", "Golf Apparel", "Golf Shoes", "Golf Bags & Carts", "Toys", "Water Sports", "Women's Golf Clubs", "Men's Golf Clubs", "Indoor/Outdoor Games"]
segments_list = ["Corporate", "Home Office", "Consumer"]
regions_list = ["South Asia", "West Asia", "South America", "East of USA", "Eastern Asia", "Western Europe", "Southeast Asia", "Northern Europe", "Central Africa", "Central America", "Caribbean", "West of USA", "US Center", "Oceania", "Central Asia", "North Africa", "East Africa", "Eastern Europe", "West Africa", "Southern Europe", "Canada", "Southern Africa", "South of  USA"]
months_list = ["July", "February", "April", "December", "September", "May", "January", "March", "June", "August", "November", "October"]

def generate_data():

    return {
        "Type": random.choice(types_list),
        "ShippingMode": random.choice(modes_list),
        "CategoryName": random.choice(categories_list),
        "CustomerSegment": random.choice(segments_list),
        "OrderItemTotal": round(random.uniform(0, 500), 2),
        "OrderRegion": random.choice(regions_list),
        "ShippingMonthName": random.choice(months_list),
    }


@app.websocket('/ws')
async def real_time_process(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = generate_data()
        await websocket.send_json(data)
        await asyncio.sleep(2)