import os
import sys

# ensure project root is on sys.path so imports work when running from `tests/`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Customer, FoodItem, Catalog, Transaction


def pretty(obj):
    try:
        return obj.__dict__
    except Exception:
        return str(obj)


if __name__ == "__main__":
    # create customer
    cust = Customer(name="Alice", email="alice@example.com", balance=50.0)
    print("Customer:", pretty(cust))

    # create food items
    burger = FoodItem(name="Spicy Burger", price=8.5, category="Entree", popularity=4.7)
    soda = FoodItem(name="Large Soda", price=2.0, category="Drinks", popularity=4.2)
    print("FoodItem 1:", pretty(burger))
    print("FoodItem 2:", pretty(soda))

    # catalog
    catalog = Catalog()
    catalog.add_item(burger)
    catalog.add_item(soda)
    print("Catalog keys:", list(catalog._items.keys()))
    print("Catalog get_item('Spicy Burger'):", pretty(catalog.get_item('Spicy Burger')))

    # transaction (build basic items list and compute total)
    cart = [
        {"item": burger, "quantity": 2},
        {"item": soda, "quantity": 1},
    ]
    total = sum(entry["item"].price * entry["quantity"] for entry in cart)
    items_snapshot = [
        {"name": entry["item"].name, "unit_price": entry["item"].price, "quantity": entry["quantity"]}
        for entry in cart
    ]
    txn = Transaction(id="txn-001", customer_id=cust.id, items=items_snapshot, total=round(total, 2))
    print("Transaction record:", txn.to_record())

    # attach to customer
    cust.add_order(txn.to_record())
    print("Customer order history:", cust.get_order_history())

    # verify user
    print("Verify first call:", cust.verify_user())
    print("Verify second call (should be False):", cust.verify_user())
