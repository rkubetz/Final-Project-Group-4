from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import resources as controller
from ..schemas import resources as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


@router.post("/", response_model=schema.Resource)
def create(resource: schema.ResourceCreate, db: Session = Depends(get_db)):
    return controller.create(db, resource)


@router.get("/", response_model=list[schema.Resource])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Resource)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)


@router.put("/{item_id}", response_model=schema.Resource)
def update(item_id: int, resource: schema.ResourceUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, resource)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)