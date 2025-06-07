import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from schemas.product import ProductCreate


def test_create_product(client: TestClient, db_session: Session):
    """Test creating a product."""
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 9.99,
        "stock_quantity": 100,
        "category": "Test Category"
    }
    
    response = client.post("/products/", json=product_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["stock_quantity"] == product_data["stock_quantity"]
    assert data["category"] == product_data["category"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_read_products(client: TestClient, db_session: Session):
    """Test getting a list of products."""
    response = client.get("/products/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    # Note: We don't assert the length because the database may already contain products


def test_read_product(client: TestClient, db_session: Session):
    """Test getting a specific product."""
    # First create a product
    product_data = {
        "name": "Test Product for Reading",
        "description": "This product is created for testing reading",
        "price": 14.99,
        "stock_quantity": 50
    }
    
    create_response = client.post("/products/", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]
    
    # Then test reading it
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["stock_quantity"] == product_data["stock_quantity"]
    assert data["id"] == product_id
