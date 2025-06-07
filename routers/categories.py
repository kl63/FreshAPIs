from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
pydantic_version = __import__('pydantic').__version__
if pydantic_version.startswith('2'):
    from pydantic import BaseModel
else:
    from pydantic.main import BaseModel

from database.database import get_db
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate, Category as CategorySchema
from core.security import get_current_admin_user, get_current_user

router = APIRouter(
    prefix="/category",
    tags=["Categories"],
    responses={404: {"description": "Not found"}},
)

# Helper function to transform category data for frontend
def transform_category(category):
    if isinstance(category, dict):
        category_dict = category
    else:
        category_dict = CategorySchema.model_validate(category).model_dump()
    
    # Add frontend-expected fields
    category_dict['_id'] = category_dict['id']  # Frontend expects _id
    
    # Frontend expects 'icon' instead of 'image_url'
    if category_dict.get('image_url'):
        category_dict['icon'] = category_dict['image_url']
    
    return category_dict

# Helper function to transform child category data - simplified for children
def transform_child_category(category):
    return {
        "_id": category.id,
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "icon": category.image_url
    }

@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    # Check if category with the same name exists
    db_category = db.query(Category).filter(Category.name == category.name).first()
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    # Create new category
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=List[CategorySchema])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

# Define a custom response model for frontend-compatible category data
class FrontendCategoryResponse(BaseModel):
    class Config:
        arbitrary_types_allowed = True

@router.get("/show")
def show_categories(db: Session = Depends(get_db)):
    """
    Get active categories in hierarchical structure for frontend display
    Returns parent categories with their children categories nested
    Transforms data to match frontend expectations (_id, icon fields)
    """
    # Get all parent categories (those with no parent_id or null parent_id)
    parent_categories = db.query(Category).filter(Category.parent_id.is_(None)).all()
    
    # Get all categories to build the hierarchy
    all_categories = db.query(Category).all()
    
    # Build a dictionary of child categories by parent_id
    children_by_parent = {}
    for category in all_categories:
        if category.parent_id is not None:
            if category.parent_id not in children_by_parent:
                children_by_parent[category.parent_id] = []
            children_by_parent[category.parent_id].append(category)
    
    # Transform categories to match frontend expectations
    transformed_categories = []
    for parent in parent_categories:
        parent_dict = transform_category(parent)
        
        # Transform child categories
        transformed_children = []
        for child in children_by_parent.get(parent.id, []):
            transformed_children.append(transform_child_category(child))
        
        parent_dict['children'] = transformed_children
        transformed_categories.append(parent_dict)
    
    return transformed_categories

@router.get("/{category_id}", response_model=CategorySchema)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int, 
    category: CategoryUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return None
