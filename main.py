# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Union

# Creamos un "diccionario" en memoria para simular una base de datos.
# Usaremos un simple contador para asignar IDs.
fake_db = {}
item_counter = 0

# Definimos el modelo de datos para los ítems de nuestra API.
# En este caso, usaremos "Items" genéricos para que se adapte a cualquier cosa.
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class ItemInDB(Item):
    id: int

app = FastAPI()

# Operaciones CRUD

# 1. Crear un nuevo ítem
@app.post("/items/", response_model=ItemInDB)
def create_item(item: Item):
    global item_counter
    item_counter += 1
    new_item = item.model_dump()
    new_item["id"] = item_counter
    fake_db[item_counter] = new_item
    return new_item

# 2. Leer todos los ítems
@app.get("/items/", response_model=List[ItemInDB])
def read_items():
    return list(fake_db.values())

# 3. Leer un ítem por su ID
@app.get("/items/{item_id}", response_model=ItemInDB)
def read_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

# 4. Actualizar un ítem
@app.put("/items/{item_id}", response_model=ItemInDB)
def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = item.model_dump()
    updated_item["id"] = item_id
    fake_db[item_id] = updated_item
    return updated_item

# 5. Eliminar un ítem
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_db[item_id]
    return {"message": "Item deleted successfully"}