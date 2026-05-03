from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import menu_items as controller
from ..schemas import menu_items as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/menu_items",
    tags=["Menu Items"]
)


@router.post("/", response_model=schema.MenuItem)
def create(item: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db, item)


@router.get("/", response_model=list[schema.MenuItem])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/search", response_model=list[schema.MenuItem])
def search_by_category(category: str, db: Session = Depends(get_db)):
    """Customer: Search available menu items by food category (e.g. vegetarian, spicy, kids, low fat)."""
    return controller.search_by_category(db, category)


@router.get("/{item_id}", response_model=schema.MenuItem)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)


@router.put("/{item_id}", response_model=schema.MenuItem)
def update(item_id: int, item: schema.MenuItemUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, item)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)