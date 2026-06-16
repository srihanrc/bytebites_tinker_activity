import os
import sys

# ensure project root is on sys.path so imports work when running from `tests/`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import FoodItem, Catalog, Transaction


def print_line(title: str) -> None:
    print("\n=== {} ===".format(title))


def main() -> None:
    catalog = Catalog()

    items = [
        FoodItem("Spicy Burger", 8.5, "Entree", 4.7),
        FoodItem("Cheese Pizza", 7.0, "Entree", 4.3),
        FoodItem("Large Soda", 2.0, "Drinks", 4.2),
        FoodItem("Chocolate Cake", 4.5, "Dessert", 4.8),
    ]

    for it in items:
        catalog.add_item(it)

    print("Catalog ids:", list(catalog._items.keys()))

    print_line("Filter: Drinks")
    drinks = catalog.filter_by_category("Drinks")
    print([(i.name, i.price) for i in drinks])

    print_line("Sort by price (asc)")
    for i in catalog.sort_items("price"):
        print(i.name, i.price)

    print_line("Sort by popularity (desc)")
    for i in catalog.sort_items("popularity", reverse=True):
        print(i.name, i.popularity)

    print_line("Query: Entree, min_price=7, sort_by=name")
    q = catalog.query(category="Entree", min_price=7, sort_by="name")
    print([(i.name, i.price) for i in q])

    # Build a transaction using FoodItem objects
    txn = Transaction(id=None, customer_id="demo-cust")
    txn.add_item(items[0], quantity=2)  # 2 Spicy Burgers
    txn.add_item(items[2], quantity=1)  # 1 Large Soda

    print_line("Transaction summary (initial)")
    for s in txn.items_summary():
        print(s)
    print("Total:", txn.compute_total())

    # Remove one burger
    txn.remove_item(items[0], quantity=1)
    print_line("Transaction summary (after removing 1 burger)")
    for s in txn.items_summary():
        print(s)
    print("Total:", txn.compute_total())

    # Update popularity
    print_line("Popularity change")
    print(items[0].name, "before:", items[0].popularity)
    items[0].update_popularity(0.5)
    print(items[0].name, "after:", items[0].popularity)


if __name__ == "__main__":
    main()
