from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API de Productos")

# Modelo Pydantic para Producto
class Product(BaseModel):
    name: str
    price: float
    category: str
    in_stock: bool = True

# Lista temporal de productos (simula base de datos)
products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 25.50, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Libro", "price": 15.00, "category": "Education", "in_stock": False}
]

# 1. GET Hello World
@app.get("/")
def hello_world() -> dict:
    return {"message": "¡Bienvenido a la API de Productos!"}

# 2. GET Todos los productos
@app.get("/products")
def get_products() -> dict:
    return {"products": products, "total": len(products)}

# 3. POST Crear producto
@app.post("/products")
def create_product(product: Product) -> dict:
    new_product = product.dict()
    new_product["id"] = len(products) + 1
    products.append(new_product)
    return {"message": "Producto creado", "product": new_product}

# 4. GET Producto por ID
@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    return {"error": "Producto no encontrado"}

# 5. GET Buscar productos
@app.get("/search")
def search_products(
    name: Optional[str] = None,
    category: Optional[str] = None,
    in_stock: Optional[bool] = None
) -> dict:
    results = products
    
    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    
    if category:
        results = [p for p in results if p["category"].lower() == category.lower()]
    
    if in_stock is not None:
        results = [p for p in results if p["in_stock"] == in_stock]
    
    return {"results": results, "count": len(results)}