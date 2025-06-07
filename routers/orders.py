from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from models.order import Order, OrderItem, OrderStatus
from models.product import Product
from schemas.order import OrderCreate, OrderUpdate, Order as OrderSchema
from core.security import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Calculate total amount
    total_amount = 0
    items_data = []
    
    for item in order.items:
        # Validate product exists and has enough stock
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found"
            )
        
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product {product.name}"
            )
        
        # Calculate item total
        item_total = item.unit_price * item.quantity
        total_amount += item_total
        
        # Update product stock
        product.stock_quantity -= item.quantity
        
        # Prepare item data
        items_data.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": item.unit_price
        })
    
    # Create order
    db_order = Order(
        user_id=current_user.id,
        status=OrderStatus.PENDING.value,
        total_amount=total_amount,
        address=order.address,
        city=order.city,
        state=order.state,
        postal_code=order.postal_code,
        country=order.country,
        phone=order.phone
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item_data in items_data:
        db_order_item = OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(db_order_item)
    
    db.commit()
    db.refresh(db_order)
    
    return db_order

@router.get("/", response_model=List[OrderSchema])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Regular users can only see their own orders
    if not current_user.is_admin:
        orders = db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(limit).all()
    else:
        # Admins can see all orders
        orders = db.query(Order).offset(skip).limit(limit).all()
    
    return orders

@router.get("/{order_id}", response_model=OrderSchema)
def read_order(order_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check permission - users can only see their own orders, admins can see all
    if not current_user.is_admin and db_order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )
    
    return db_order

@router.put("/{order_id}", response_model=OrderSchema)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check permission - only admins can update any order, users can only update their own orders
    if not current_user.is_admin and db_order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this order"
        )
    
    # Additional restriction: only admins can change order status
    update_data = order.model_dump(exclude_unset=True)
    if "status" in update_data and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can change order status"
        )
    
    # Update order fields
    for key, value in update_data.items():
        setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(order_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check permission - only admins can delete any order, users can only delete their own pending orders
    if not current_user.is_admin and (db_order.user_id != current_user.id or db_order.status != OrderStatus.PENDING.value):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this order"
        )
    
    # Instead of deleting, change status to CANCELLED
    db_order.status = OrderStatus.CANCELLED.value
    
    # Return items to inventory
    for item in db_order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_quantity += item.quantity
    
    db.commit()
    return None
