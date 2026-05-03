import pytest
from unittest.mock import MagicMock
from datetime import datetime

# Import controllers to test
from api.controllers import orders as order_controller
from api.controllers import menu_items as menu_controller
from api.controllers import promo_codes as promo_controller
from api.models import orders as order_model
from api.models import menu_items as menu_model
from api.models import promo_codes as promo_model


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def db():
    """Mock database session."""
    return MagicMock()


# ─── Order Tests ──────────────────────────────────────────────────────────────

def test_create_order(db):
    """Test that create() adds a new order and returns it."""
    request = MagicMock()
    request.order_number = "ORD-001"
    request.customer_name = "Jane Smith"
    request.customer_phone = "704-555-0100"
    request.customer_address = "123 Main St"
    request.order_type = "delivery"
    request.order_date = datetime.utcnow()
    request.total_price = 29.99
    request.order_status = "pending"
    request.promo_code = None

    # Simulate db.refresh populating the id
    def fake_refresh(obj):
        obj.id = 1

    db.refresh.side_effect = fake_refresh

    result = order_controller.create(db, request)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    assert result.customer_name == "Jane Smith"
    assert result.order_number == "ORD-001"
    assert result.order_type == "delivery"


def test_read_all_orders(db):
    """Test that read_all() returns list of orders from db."""
    mock_orders = [MagicMock(), MagicMock()]
    db.query.return_value.all.return_value = mock_orders

    result = order_controller.read_all(db)

    assert result == mock_orders
    assert len(result) == 2


def test_track_order_by_number_found(db):
    """Test tracking an order by its tracking number."""
    mock_order = MagicMock()
    mock_order.order_number = "ORD-001"
    mock_order.customer_name = "Jane Smith"
    mock_order.order_status = "in progress"
    mock_order.order_type = "delivery"
    mock_order.order_date = datetime.utcnow()
    mock_order.total_price = 29.99

    db.query.return_value.filter.return_value.first.return_value = mock_order

    result = order_controller.track_by_order_number(db, "ORD-001")

    assert result["order_number"] == "ORD-001"
    assert result["order_status"] == "in progress"


def test_track_order_not_found(db):
    """Test that tracking a nonexistent order raises 404."""
    from fastapi import HTTPException
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        order_controller.track_by_order_number(db, "FAKE-999")

    assert exc_info.value.status_code == 404


# ─── Menu Item Tests ──────────────────────────────────────────────────────────

def test_create_menu_item(db):
    """Test that a menu item is created and returned."""
    request = MagicMock()
    request.name = "Veggie Burger"
    request.calorie_count = 450
    request.price = 9.99
    request.category = "vegetarian"
    request.available = True

    def fake_refresh(obj):
        obj.id = 5

    db.refresh.side_effect = fake_refresh

    result = menu_controller.create(db, request)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    assert result.name == "Veggie Burger"
    assert result.category == "vegetarian"


def test_search_by_category(db):
    """Test that search_by_category filters correctly."""
    mock_items = [MagicMock(name="Veggie Burger", category="vegetarian")]
    db.query.return_value.filter.return_value.all.return_value = mock_items

    result = menu_controller.search_by_category(db, "vegetarian")

    assert result == mock_items


# ─── Promo Code Tests ─────────────────────────────────────────────────────────

def test_validate_promo_code_valid(db):
    """Test that a valid promo code returns its discount info."""
    mock_promo = MagicMock()
    mock_promo.code = "SAVE10"
    mock_promo.discount_percent = 10.0
    mock_promo.expiration_date = datetime(2099, 12, 31)

    db.query.return_value.filter.return_value.first.return_value = mock_promo

    result = promo_controller.validate_code(db, "SAVE10")

    assert result["code"] == "SAVE10"
    assert result["discount_percent"] == 10.0


def test_validate_promo_code_invalid(db):
    """Test that an invalid/expired promo code raises 404."""
    from fastapi import HTTPException
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        promo_controller.validate_code(db, "BADCODE")

    assert exc_info.value.status_code == 404