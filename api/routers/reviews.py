from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import reviews as controller
from ..schemas import reviews as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)



@router.post("/", response_model=schema.Review)
def create(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Review])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/menu_item/{menu_item_id}", response_model=list[schema.Review])
def read_by_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a specific menu item (for customers to browse)."""
    return controller.read_by_menu_item(db, menu_item_id)


@router.get("/{item_id}", response_model=schema.Review)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)


@router.put("/{item_id}", response_model=schema.Review)
def update(item_id: int, request: schema.ReviewUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)