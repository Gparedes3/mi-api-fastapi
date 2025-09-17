# main.py
from fastapi import FastAPI

app = FastAPI()

db = {}
counter = 0

@app.post("/items/")
def create_item(item: dict):
    global counter
    counter += 1
    item["id"] = counter
    db[counter] = item
    return item

@app.get("/items/")
def read_items():
    return list(db.values())

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return db[item_id]

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    item["id"] = item_id
    db[item_id] = item
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    del db[item_id]
    return {"message": "Deleted"}
