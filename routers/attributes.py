from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database.database import get_db
from models.attribute import Attribute, AttributeValue
from schemas.attribute import Attribute as AttributeSchema
from schemas.attribute import AttributeCreate, AttributeUpdate
from core.security import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/attributes",
    tags=["attributes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[AttributeSchema])
async def get_all_attributes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get all attributes with pagination"""
    attributes = db.query(Attribute).offset(skip).limit(limit).all()
    return attributes

@router.get("/show", response_model=List[AttributeSchema])
async def get_showing_attributes(
    db: Session = Depends(get_db)
):
    """Get all active attributes for display in the store"""
    attributes = db.query(Attribute).filter(Attribute.is_active == True).all()
    
    # If no attributes exist, create some default ones
    if len(attributes) == 0:
        # Create Size attribute
        size_attr = Attribute(
            name="Size",
            slug="size",
            display_name="Size",
            description="Product size options",
            is_active=True
        )
        db.add(size_attr)
        db.flush()  # Flush to get the ID
        
        # Add size values
        sizes = ["Small", "Medium", "Large"]
        for size in sizes:
            size_value = AttributeValue(
                name=size,
                value=size.lower(),
                attribute_id=size_attr.id,
                is_active=True
            )
            db.add(size_value)
        
        # Create Color attribute
        color_attr = Attribute(
            name="Color",
            slug="color",
            display_name="Color",
            description="Product color options",
            is_active=True
        )
        db.add(color_attr)
        db.flush()  # Flush to get the ID
        
        # Add color values
        colors = ["Red", "Blue", "Green", "Yellow", "Black", "White"]
        for color in colors:
            color_value = AttributeValue(
                name=color,
                value=color.lower(),
                attribute_id=color_attr.id,
                is_active=True
            )
            db.add(color_value)
        
        db.commit()
        
        # Fetch the newly created attributes
        attributes = db.query(Attribute).filter(Attribute.is_active == True).all()
    
    return attributes

@router.get("/{attribute_id}", response_model=AttributeSchema)
async def get_attribute_by_id(
    attribute_id: int,
    db: Session = Depends(get_db)
):
    """Get attribute by ID"""
    attribute = db.query(Attribute).filter(Attribute.id == attribute_id).first()
    if not attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    return attribute

@router.post("/", response_model=AttributeSchema, status_code=status.HTTP_201_CREATED)
async def create_attribute(
    attribute: AttributeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """Create a new attribute (admin only)"""
    # Check if attribute with same slug already exists
    existing = db.query(Attribute).filter(Attribute.slug == attribute.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attribute with this slug already exists"
        )
    
    # Create new attribute
    db_attribute = Attribute(
        name=attribute.name,
        slug=attribute.slug,
        display_name=attribute.display_name,
        description=attribute.description,
        is_active=attribute.is_active
    )
    db.add(db_attribute)
    db.flush()
    
    # Create attribute values if provided
    for value in attribute.values:
        db_value = AttributeValue(
            name=value.name,
            value=value.value,
            is_active=value.is_active,
            attribute_id=db_attribute.id
        )
        db.add(db_value)
    
    db.commit()
    db.refresh(db_attribute)
    return db_attribute

@router.put("/{attribute_id}", response_model=AttributeSchema)
async def update_attribute(
    attribute_id: int,
    attribute_update: AttributeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """Update an attribute (admin only)"""
    db_attribute = db.query(Attribute).filter(Attribute.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    
    # Update attribute fields if provided in the request
    update_data = attribute_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_attribute, field, value)
    
    db.commit()
    db.refresh(db_attribute)
    return db_attribute

@router.delete("/{attribute_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attribute(
    attribute_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """Delete an attribute (admin only)"""
    db_attribute = db.query(Attribute).filter(Attribute.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    
    db.delete(db_attribute)
    db.commit()
    return None
