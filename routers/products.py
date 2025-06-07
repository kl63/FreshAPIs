from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_, and_

from database.database import get_db
from models.product import Product
from models.category import Category
from schemas.product import ProductCreate, ProductUpdate, Product as ProductSchema

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}},
)

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List as PyList

# Helper function to transform product data
def transform_product(product):
    product_dict = ProductSchema.model_validate(product).model_dump()
    
    # Add frontend-expected fields
    product_dict['_id'] = product_dict['id']  # Frontend expects _id
    product_dict['title'] = product_dict['name']  # Frontend expects title
    
    # Create prices object structure expected by frontend
    product_dict['prices'] = {
        'price': product_dict['price'],
        'originalPrice': product_dict.get('discounted_price', 0) if product_dict.get('discounted_price', 0) > 0 else product_dict['price']
    }
    
    # Create image array from image_url
    if product_dict.get('image_url'):
        product_dict['image'] = [product_dict['image_url']]
    else:
        product_dict['image'] = []
        
    return product_dict

class ProductResponse(BaseModel):
    popularProducts: PyList[ProductSchema] = []
    discountedProducts: PyList[ProductSchema] = []

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Transform product to include image array
    return transform_product(db_product)

@router.get("/")
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    # Transform products to include image array
    return [transform_product(p) for p in products]

@router.get("/store")
def get_store_products(
    category: Optional[str] = Query(None, description="Category ID or slug"),
    title: Optional[str] = Query(None, description="Search by product title"),
    slug: Optional[str] = Query(None, description="Search by product slug"),
    skip: int = 0, 
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get products for store display with filtering options"""
    query = db.query(Product).filter(Product.availability == True)
    
    # Filter by category if provided
    if category and category != "":
        # Check if category parameter is numeric (ID) or string (slug)
        try:
            category_id = int(category)
            query = query.filter(Product.category_id == category_id)
        except ValueError:
            # If not numeric, treat as slug
            category_obj = db.query(Category).filter(Category.slug == category).first()
            if category_obj:
                query = query.filter(Product.category_id == category_obj.id)
    
    # Filter by title if provided
    if title and title != "":
        search = f"%{title}%"
        query = query.filter(Product.name.ilike(search))
    
    # Filter by slug if provided
    if slug and slug != "":
        query = query.filter(Product.slug == slug)
    
    # Get the filtered products
    filtered_products = query.order_by(Product.created_at.desc()).offset(skip).limit(limit).all()
    
    # Get popular products (most recent)
    popular_products = db.query(Product)\
        .filter(Product.availability == True)\
        .order_by(Product.created_at.desc())\
        .limit(10)\
        .all()
    
    # Get discounted products
    discounted_products = db.query(Product)\
        .filter(and_(Product.availability == True, Product.discounted_price > 0))\
        .order_by(Product.created_at.desc())\
        .limit(10)\
        .all()
    
    # Transform all products to include the image array
    popular_products_transformed = [transform_product(p) for p in popular_products]
    discounted_products_transformed = [transform_product(p) for p in discounted_products]
    filtered_products_transformed = [transform_product(p) for p in filtered_products]
    
    # Return the expected structure
    return {
        "popularProducts": popular_products_transformed,
        "discountedProducts": discounted_products_transformed,
        "products": filtered_products_transformed  # Include the filtered products as well
    }

@router.get("/show")
def get_showing_products(db: Session = Depends(get_db), limit: int = 10):
    """Get products for display on home page or featured sections"""
    products = db.query(Product)\
        .filter(Product.availability == True)\
        .order_by(Product.created_at.desc())\
        .limit(limit)\
        .all()
    # Transform products to include image array
    return [transform_product(p) for p in products]

@router.get("/discount")
def get_discounted_products(db: Session = Depends(get_db), limit: int = 10):
    """Get products with discount"""
    products = db.query(Product)\
        .filter(and_(Product.availability == True, Product.discounted_price > 0))\
        .order_by(Product.created_at.desc())\
        .limit(limit)\
        .all()
    # Transform products to include image array
    return [transform_product(p) for p in products]

@router.get("/{product_id_or_slug}")
def read_product(product_id_or_slug: str, db: Session = Depends(get_db)):
    # Try to parse as integer (ID)
    try:
        product_id = int(product_id_or_slug)
        db_product = db.query(Product).filter(Product.id == product_id).first()
    except ValueError:
        # If not an integer, try to find by slug
        db_product = db.query(Product).filter(Product.slug == product_id_or_slug).first()
    
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Transform product to include image array
    return transform_product(db_product)

@router.put("/{product_id}")
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
        
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
            
    db.commit()
    db.refresh(db_product)
    # Transform product to include image array
    return transform_product(db_product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
        
    db.delete(db_product)
    db.commit()
    return None
