import pytest
from datetime import datetime
from domain.models.order import Order, OrderStatus
from domain.models.item_order import ItemOrder
from domain.models.product import Product


# ---------------------------
# Fixtures auxiliares
# ---------------------------

@pytest.fixture
def product1():
    return Product(
        id=1,
        name="Pizza",
        price=30.0,
        availability=True,
        category="Food",
        imageUrl="https://example.com/pizza.jpg",
        visibility=True,
    )


@pytest.fixture
def product2():
    return Product(
        id=2,
        name="Refrigerante",
        price=8.0,
        availability=True,
        category="Drink",
        imageUrl="https://example.com/drink.jpg",
        visibility=True,
    )


@pytest.fixture
def order():
    return Order(id=1, table_number=10, waiter_id=5)


# ---------------------------
# Testes do total_price
# ---------------------------

def test_total_price_empty_order(order):
    assert order.total_price == 0


def test_total_price_with_items(order, product1, product2):
    order.add_item(product1, quantity=2)  # 2 * 30 = 60
    order.add_item(product2, quantity=3)  # 3 * 8  = 24
    assert order.total_price == 84


# ---------------------------
# Testes do add_item
# ---------------------------

def test_add_item_new_product(order, product1):
    order.add_item(product1, quantity=2)
    assert len(order.items) == 1
    assert order.items[0].quantity == 2
    assert order.items[0].product.id == 1


def test_add_item_existing_product_increments(order, product1):
    order.add_item(product1, 1)
    order.add_item(product1, 3)
    assert len(order.items) == 1
    assert order.items[0].quantity == 4  # incrementou corretamente


def test_add_item_zero_or_negative_quantity(order, product1):
    with pytest.raises(ValueError):
        order.add_item(product1, quantity=0)
    with pytest.raises(ValueError):
        order.add_item(product1, quantity=-1)


def test_add_item_on_completed_order(order, product1):
    order.mark_as_in_progress()
    order.mark_as_completed()
    with pytest.raises(ValueError):
        order.add_item(product1, 1)


def test_add_item_on_cancelled_order(order, product1):
    order.mark_as_cancelled()
    with pytest.raises(ValueError):
        order.add_item(product1, 1)


# ---------------------------
# Testes do remove_product
# ---------------------------

def test_remove_existing_product(order, product1, product2):
    order.add_item(product1, 1)
    order.add_item(product2, 1)
    
    order.remove_product(product1.id)
    assert len(order.items) == 1
    assert order.items[0].product.id == product2.id


def test_remove_nonexistent_product_raises(order):
    with pytest.raises(ValueError):
        order.remove_product(999)


def test_remove_product_on_completed_order(order, product1):
    order.add_item(product1, 1)
    order.mark_as_in_progress()
    order.mark_as_completed()

    with pytest.raises(ValueError):
        order.remove_product(product1.id)


def test_remove_product_on_cancelled_order(order, product1):
    order.add_item(product1, 1)
    order.mark_as_cancelled()

    with pytest.raises(ValueError):
        order.remove_product(product1.id)


# ---------------------------
# Testes de mudança de status
# ---------------------------

def test_mark_as_in_progress(order):
    order.mark_as_in_progress()
    assert order.status == OrderStatus.IN_PROGRESS


def test_mark_as_in_progress_invalid(order):
    order.mark_as_in_progress()
    with pytest.raises(ValueError):
        order.mark_as_in_progress()  # não pode duas vezes


def test_mark_as_completed(order):
    order.mark_as_in_progress()
    order.mark_as_completed()
    assert order.status == OrderStatus.COMPLETED


def test_mark_as_completed_invalid(order):
    with pytest.raises(ValueError):  # não está em IN_PROGRESS
        order.mark_as_completed()


def test_mark_as_cancelled(order):
    order.mark_as_cancelled()
    assert order.status == OrderStatus.CANCELLED


def test_mark_as_cancelled_invalid_if_completed(order):
    order.mark_as_in_progress()
    order.mark_as_completed()

    with pytest.raises(ValueError):
        order.mark_as_cancelled()
