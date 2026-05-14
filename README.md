# FastAPI Product API Assignment

## Project Overview

This project is a Product Management API built using FastAPI and MongoDB.
It includes:

* Product Creation API
* Get Product By ID API
* Get Products By Category API (Query Parameter)
* Delete Product API
* Health Check API
* MongoDB Integration
* Environment Variables
* Pydantic Validation
* Error Handling
* Swagger Documentation

---

# Project Structure

```text
product-api/
│
├── .venv/
│
├── .env
│
├── requirements.txt
│
├── README.md
│
└── main.py
```

---

# 1. Create Virtual Environment

## Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

# 2. requirements.txt

Create a file named `requirements.txt`

```txt
fastapi
uvicorn
pymongo
python-dotenv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 3. Run the FastAPI Server

```bash
uvicorn main:app --reload
```

---

# 4. Swagger Documentation

Open browser:

```text
http://127.0.0.1:8000/docs
```

---

# 5. API Endpoints

| Method | Endpoint                       | Description              |
| ------ | ------------------------------ | ------------------------ |
| POST   | /products                      | Create product           |
| GET    | /products/{product_id}         | Get product by ID        |
| GET    | /products?category=Electronics | Get products by category |
| DELETE | /products/{product_id}         | Delete product           |
| GET    | /health                        | Health check API         |

---

# 6. Example Request Body

## POST /products

```json
{
  "product_name": "iPhone 15",
  "category": "Electronics",
  "price": 85000
}
```

---

# 7. Example Success Response

```json
{
  "success": true,
  "message": "Product created successfully",
  "data": {
    "id": "68230d123456789",
    "product_name": "iPhone 15",
    "category": "Electronics",
    "price": 85000
  }
}
```

---

# 8. Example Error Response

```json
{
  "detail": "Product not found"
}
```

---

# 9. MongoDB Commands

Open Mongo Shell:

```bash
mongosh
```

Show databases:

```bash
show dbs
```

Use database:

```bash
use product_db
```

Show collections:

```bash
show collections
```

View inserted products:

```bash
db.products.find().pretty()
```

---
