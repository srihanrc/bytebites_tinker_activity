import os
import sys
import pytest

# ensure project root is on sys.path so imports work when running tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Customer, FoodItem, Catalog, Transaction


def test_models_import_and_basic_workflow():
	# basic instantiation smoke test to ensure imports work
	cust = Customer(name="Test", email="t@example.com", balance=0.0)
	item = FoodItem(name="Sample", price=1.5, category="Snack", popularity=3.0)
	catalog = Catalog()
	catalog.add_item(item)
	txn = Transaction(id="t-1", customer_id=cust.id, items=[{"name": item.name, "unit_price": item.price, "quantity": 1}])
	assert txn.compute_total() == 1.5
	cust.add_order(txn.to_record())
	assert len(cust.get_order_history()) == 1


def test_price_addition_rounding():
	a = FoodItem("A", 0.1, "Snack", 0.0)
	b = FoodItem("B", 0.2, "Snack", 0.0)
	txn = Transaction(id=None, customer_id="c")
	txn.add_item(a, 1)
	txn.add_item(b, 1)
	assert txn.compute_total() == 0.3


def test_aggregation_and_partial_removal():
	item = FoodItem("X", 2.5, "Snack", 0.0)
	txn = Transaction(id=None, customer_id="c")
	txn.add_item(item, 2)
	assert txn.compute_total() == 5.0
	txn.add_item(item, 3)
	assert txn.compute_total() == 12.5
	removed = txn.remove_item(item, quantity=2)
	assert removed is True
	assert txn.compute_total() == 7.5
	removed2 = txn.remove_item(item, quantity=10)
	assert removed2 is True
	assert txn.compute_total() == 0.0


def test_invalid_quantity_raises():
	item = FoodItem("Y", 1.0, "Snack", 0.0)
	txn = Transaction(id=None, customer_id="c")
	with pytest.raises(ValueError):
		txn.add_item(item, 0)
	with pytest.raises(ValueError):
		txn.remove_item(item, 0)


def test_catalog_search_and_query():
	catalog = Catalog()
	a = FoodItem("Spicy Burger", 8.5, "Entree", 4.7)
	b = FoodItem("large soda", 2.0, "Drinks", 4.2)
	catalog.add_item(a)
	catalog.add_item(b)
	assert catalog.find_item_by_name("spicy burger").id == a.id
	assert catalog.find_item_by_name("LARGE SODA").id == b.id
	q = catalog.query(min_price=2.0, max_price=8.5)
	assert set(i.name for i in q) == {a.name, b.name}
	drinks = catalog.filter_by_category("drinks")
	assert len(drinks) == 1 and drinks[0].name == b.name


def test_update_popularity_clamp():
	item = FoodItem("Z", 1.0, popularity=1.0)
	item.update_popularity(-5)
	assert item.popularity == 0.0


def test_remove_item_return_values():
	item = FoodItem("M", 3.0)
	txn = Transaction(id=None, customer_id="c")
	txn.add_item(item, 1)
	assert txn.remove_item(item, 1) is True
	assert txn.remove_item(item, 1) is False


def test_order_totals_multiple_items():
	burger = FoodItem("Burger", 8.5, "Entree", 4.0)
	soda = FoodItem("Soda", 2.25, "Drinks", 3.5)
	txn = Transaction(id=None, customer_id="c")
	txn.add_item(burger, 2)
	txn.add_item(soda, 3)
	# 2*8.5 + 3*2.25 = 17.0 + 6.75 = 23.75
	assert txn.compute_total() == 23.75


def test_empty_transaction_total_and_summary():
	txn = Transaction(id=None, customer_id="c")
	assert txn.compute_total() == 0.0
	assert txn.items_summary() == []


def test_filter_menu_items_by_category():
	catalog = Catalog()
	items = [
		FoodItem("I1", 1.0, "Drinks"),
		FoodItem("I2", 2.0, "Dessert"),
		FoodItem("I3", 3.0, "Drinks"),
	]
	for it in items:
		catalog.add_item(it)
	drinks = catalog.filter_by_category("Drinks")
	assert set(i.name for i in drinks) == {"I1", "I3"}
