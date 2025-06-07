from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database.database import get_db
from models.coupon import Coupon
from schemas.coupon import CouponCreate, CouponUpdate, Coupon as CouponSchema

router = APIRouter(
    prefix="/coupon",
    tags=["Coupons"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CouponSchema, status_code=status.HTTP_201_CREATED)
def create_coupon(coupon: CouponCreate, db: Session = Depends(get_db)):
    db_coupon = Coupon(**coupon.model_dump())
    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)
    return db_coupon

@router.get("/", response_model=List[CouponSchema])
def get_all_coupons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    coupons = db.query(Coupon).offset(skip).limit(limit).all()
    return coupons

@router.get("/show", response_model=List[CouponSchema])
def get_showing_coupons(db: Session = Depends(get_db)):
    """Get active coupons for the store front"""
    now = datetime.now()
    coupons = db.query(Coupon).filter(
        Coupon.active == True,
        (Coupon.start_date <= now) | (Coupon.start_date == None),
        (Coupon.end_date >= now) | (Coupon.end_date == None)
    ).all()
    return coupons

@router.get("/{coupon_id}", response_model=CouponSchema)
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if db_coupon is None:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return db_coupon

@router.put("/{coupon_id}", response_model=CouponSchema)
def update_coupon(coupon_id: int, coupon: CouponUpdate, db: Session = Depends(get_db)):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if db_coupon is None:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    update_data = coupon.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_coupon, key, value)
    
    db.commit()
    db.refresh(db_coupon)
    return db_coupon

@router.delete("/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon(coupon_id: int, db: Session = Depends(get_db)):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if db_coupon is None:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    db.delete(db_coupon)
    db.commit()
    return None
