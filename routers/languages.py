from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from models.language import Language
from schemas.language import Language as LanguageSchema, LanguageCreate, LanguageUpdate
from core.security import get_current_admin_user

router = APIRouter(
    prefix="/language",
    tags=["Languages"],
    responses={404: {"description": "Not found"}},
)

# Initialize default languages if none exist
async def get_or_create_default_language(db: Session):
    # Check if we already have languages
    db_languages = db.query(Language).all()
    if not db_languages:
        # Create English as default language
        english = Language(
            name="English",
            code="en",
            flag="/flags/en.png",
            is_default=True,
            is_active=True
        )
        db.add(english)
        
        # Create Spanish as additional language
        spanish = Language(
            name="Spanish",
            code="es",
            flag="/flags/es.png",
            is_default=False,
            is_active=True
        )
        db.add(spanish)
        
        db.commit()
    
    # Get active languages
    return db.query(Language).filter(Language.is_active == True).all()

@router.get("/show", response_model=List[LanguageSchema])
async def get_active_languages(db: Session = Depends(get_db)):
    """Get all active languages"""
    languages = await get_or_create_default_language(db)
    return languages

@router.get("/all", response_model=List[LanguageSchema])
async def get_all_languages(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """Get all languages (admin only)"""
    languages = db.query(Language).all()
    return languages

@router.post("/", response_model=LanguageSchema, status_code=status.HTTP_201_CREATED)
async def create_language(
    language: LanguageCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """Create a new language (admin only)"""
    # Check if language code already exists
    db_language = db.query(Language).filter(Language.code == language.code).first()
    if db_language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Language with code '{language.code}' already exists"
        )
    
    # If this is set as default, unset other defaults
    if language.is_default:
        db.query(Language).filter(Language.is_default == True).update({
            "is_default": False
        })
    
    # Create new language
    db_language = Language(**language.model_dump())
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    
    return db_language

@router.get("/{language_id}", response_model=LanguageSchema)
async def get_language(
    language_id: int,
    db: Session = Depends(get_db)
):
    """Get language details"""
    db_language = db.query(Language).filter(Language.id == language_id).first()
    if not db_language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found"
        )
    
    return db_language

@router.put("/{language_id}", response_model=LanguageSchema)
async def update_language(
    language_id: int,
    language: LanguageUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """Update a language (admin only)"""
    db_language = db.query(Language).filter(Language.id == language_id).first()
    if not db_language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found"
        )
    
    # If setting as default, unset other defaults
    update_data = language.model_dump(exclude_unset=True)
    if update_data.get("is_default"):
        db.query(Language).filter(Language.is_default == True).update({
            "is_default": False
        })
    
    # Update fields
    for key, value in update_data.items():
        setattr(db_language, key, value)
    
    db.commit()
    db.refresh(db_language)
    
    return db_language

@router.delete("/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_language(
    language_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """Delete a language (admin only)"""
    db_language = db.query(Language).filter(Language.id == language_id).first()
    if not db_language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found"
        )
    
    # Don't allow deleting the default language
    if db_language.is_default:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete the default language"
        )
    
    db.delete(db_language)
    db.commit()
    
    return None
