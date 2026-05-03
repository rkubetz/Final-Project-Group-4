from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import promo_codes as controller
from ..schemas import promo_codes as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/promo_codes",
    tags=["Promo Codes"]
)


@router.post("/", response_model=schema.PromoCode)
def create(promo: schema.PromoCodeCreate, db: Session = Depends(get_db)):
    return controller.create(db, promo)


@router.get("/", response_model=list[schema.PromoCode])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/validate/{code}")
def validate_code(code: str, db: Session = Depends(get_db)):
    """Validate a promo code and return its discount percentage."""
    return controller.validate_code(db, code)


@router.get("/{item_id}", response_model=schema.PromoCode)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)


@router.put("/{item_id}", response_model=schema.PromoCode)
def update(item_id: int, promo: schema.PromoCodeUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, promo)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)