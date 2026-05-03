from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from fastapi import HTTPException, status, Response
from ..models import orders as model
from ..models import order_details as detail_model
from ..models import menu_items as menu_model
from ..models import reviews as review_model
from ..models import resources as resource_model
from ..models import recipes as recipe_model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def create(db: Session, request):
    new_item = model.Order(
        order_number=request.order_number,
        customer_name=request.customer_name,
        customer_phone=request.customer_phone,
        customer_address=request.customer_address,
        order_type=request.order_type,
        order_date=request.order_date,
        total_price=request.total_price,
        order_status=request.order_status,
        promo_code=request.promo_code
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def track_by_order_number(db: Session, order_number: str):
    """Customer tracks their order by tracking number (order_number)."""
    item = db.query(model.Order).filter(model.Order.order_number == order_number).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No order found with tracking number {order_number}")
    return {
        "order_number": item.order_number,
        "customer_name": item.customer_name,
        "order_status": item.order_status,
        "order_type": item.order_type,
        "order_date": item.order_date,
        "total_price": item.total_price
    }


def read_by_date_range(db: Session, start_date: datetime, end_date: datetime):
    """Staff: view orders within a specific date range."""
    try:
        result = db.query(model.Order).filter(
            model.Order.order_date >= start_date,
            model.Order.order_date <= end_date
        ).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def get_daily_revenue(db: Session, date: str):
    """Staff: get total revenue for a given date (YYYY-MM-DD)."""
    try:
        target = datetime.strptime(date, "%Y-%m-%d").date()
        total = db.query(func.sum(model.Order.total_price)).filter(
            cast(model.Order.order_date, Date) == target
        ).scalar()
        return {"date": date, "total_revenue": round(total or 0.0, 2)}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid date format. Use YYYY-MM-DD.")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def check_ingredient_availability(db: Session, menu_item_id: int):
    """Staff: check if there are sufficient ingredients to fulfill one serving of a menu item."""
    recipes = db.query(recipe_model.Recipe).filter(
        recipe_model.Recipe.menu_item_id == menu_item_id
    ).all()
    if not recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No recipe found for this menu item.")
    issues = []
    for recipe in recipes:
        resource = db.query(resource_model.Resource).filter(
            resource_model.Resource.id == recipe.resource_id
        ).first()
        if resource is None or resource.amount < recipe.amount:
            available = resource.amount if resource else 0
            issues.append({
                "ingredient_id": recipe.resource_id,
                "ingredient_name": resource.item if resource else "Unknown",
                "required": recipe.amount,
                "available": available
            })
    if issues:
        return {"sufficient": False, "shortages": issues}
    return {"sufficient": True, "shortages": []}


def get_low_rated_items(db: Session, threshold: float = 3.0):
    """Staff: identify dishes with average rating below threshold or with complaints."""
    results = (
        db.query(
            menu_model.MenuItem.id,
            menu_model.MenuItem.name,
            func.avg(review_model.Review.rating).label("avg_rating"),
            func.count(review_model.Review.id).label("review_count")
        )
        .join(review_model.Review, review_model.Review.menu_item_id == menu_model.MenuItem.id)
        .group_by(menu_model.MenuItem.id, menu_model.MenuItem.name)
        .having(func.avg(review_model.Review.rating) <= threshold)
        .all()
    )
    return [
        {
            "menu_item_id": r.id,
            "name": r.name,
            "avg_rating": round(float(r.avg_rating), 2),
            "review_count": r.review_count
        }
        for r in results
    ]


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)