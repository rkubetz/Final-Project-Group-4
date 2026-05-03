from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db
from datetime import datetime

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/revenue/daily")
def get_daily_revenue(date: str, db: Session = Depends(get_db)):
    """Staff: Get total revenue for a given date. Format: YYYY-MM-DD"""
    return controller.get_daily_revenue(db, date)
 
 
@router.get("/date_range", response_model=list[schema.Order])
def read_by_date_range(start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    """Staff: Get all orders between start_date and end_date."""
    return controller.read_by_date_range(db, start_date, end_date)
 
 
@router.get("/low_rated_items")
def get_low_rated_items(threshold: float = 3.0, db: Session = Depends(get_db)):
    """Staff: Identify dishes with low ratings or complaints (avg rating <= threshold)."""
    return controller.get_low_rated_items(db, threshold)
 
 
@router.get("/ingredient_check/{menu_item_id}")
def check_ingredient_availability(menu_item_id: int, db: Session = Depends(get_db)):
    """Staff: Check whether sufficient ingredients exist for a given menu item."""
    return controller.check_ingredient_availability(db, menu_item_id)
 
 
# --- Customer Endpoints ---
 
@router.get("/track/{order_number}")
def track_order(order_number: str, db: Session = Depends(get_db)):
    """Customer: Track order status by tracking number."""
    return controller.track_by_order_number(db, order_number)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
