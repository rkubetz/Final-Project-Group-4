from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import payment_info as controller
from ..schemas import payment_info as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/payment_information",
    tags=["Payment Information"]
)


@router.post("/", response_model=schema.PaymentInformation)
def create(payment: schema.PaymentInformationCreate, db: Session = Depends(get_db)):
    return controller.create(db, payment)


@router.get("/", response_model=list[schema.PaymentInformation])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.PaymentInformation)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)


@router.put("/{item_id}", response_model=schema.PaymentInformation)
def update(item_id: int, payment: schema.PaymentInformationUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, payment)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)