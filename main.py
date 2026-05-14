from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# =========================
# DATABASE CONNECTION
# =========================

try:
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    product_collection = db[COLLECTION_NAME]

    print("MongoDB Connected Successfully")

except Exception as e:
    print("Database Connection Error:", e)

# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="Product API",
    description="FastAPI Product CRUD API with MongoDB",
    version="1.0.0"
)

# =========================
# PYDANTIC MODEL
# =========================

class Product(BaseModel):
    product_name: str = Field(..., min_length=2)
    category: str
    price: float = Field(..., gt=0)

# =========================
# HELPER FUNCTION
# =========================

def serialize_product(product) -> dict:
    return {
        "id": str(product["_id"]),
        "product_name": product["product_name"],
        "category": product["category"],
        "price": product["price"]
    }

# =========================
# HEALTH CHECK API
# =========================

@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "API is running successfully"
    }

# =========================
# CREATE PRODUCT API
# =========================

@app.post("/products")
def create_product(product: Product):

    try:
        product_data = product.dict()

        inserted_product = product_collection.insert_one(product_data)

        created_product = product_collection.find_one(
            {"_id": inserted_product.inserted_id}
        )

        return {
            "success": True,
            "message": "Product created successfully",
            "data": serialize_product(created_product)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating product: {str(e)}"
        )

# =========================
# GET PRODUCT BY ID API
# =========================

@app.get("/products/{product_id}")
def get_product(product_id: str):

    try:
        if not ObjectId.is_valid(product_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid Product ID"
            )

        product = product_collection.find_one(
            {"_id": ObjectId(product_id)}
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return {
            "success": True,
            "data": serialize_product(product)
        }

    except HTTPException as http_error:
        raise http_error

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching product: {str(e)}"
        )

# =========================
# GET PRODUCTS BY CATEGORY
# QUERY PARAM API
# =========================

@app.get("/products")
def get_products_by_category(
    category: str = Query(..., description="Enter category name")
):

    try:
        products = list(
            product_collection.find(
                {"category": {"$regex": category, "$options": "i"}}
            )
        )

        if not products:
            raise HTTPException(
                status_code=404,
                detail="No products found for this category"
            )

        return {
            "success": True,
            "count": len(products),
            "data": [serialize_product(product) for product in products]
        }

    except HTTPException as http_error:
        raise http_error

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching products: {str(e)}"
        )

# =========================
# DELETE PRODUCT API
# EXTRA FEATURE
# =========================

@app.delete("/products/{product_id}")
def delete_product(product_id: str):

    try:
        if not ObjectId.is_valid(product_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid Product ID"
            )

        deleted_product = product_collection.delete_one(
            {"_id": ObjectId(product_id)}
        )

        if deleted_product.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return {
            "success": True,
            "message": "Product deleted successfully"
        }

    except HTTPException as http_error:
        raise http_error

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting product: {str(e)}"
        )