"""ByteBites models: Customer, FoodItem, Catalog, Transaction.

First-draft implementations for filtering, sorting, totals, and helpers.
"""

from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid


class Customer:
    def __init__(self, name: str, email: str, balance: float = 0.0, id: Optional[str] = None) -> None:
        self.id: str = id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.balance = float(balance)
        self.order_history: List[Dict[str, Any]] = []
        self.verified: bool = False

    # Backwards-compatible method (existing demos call this)
    def verify_user(self) -> bool:
        if getattr(self, "verified", False):
            return False
        self.verified = True
        return True

    # New name aligned with spec
    def verify_identity(self) -> bool:
        return self.verify_user()

    def add_order(self, txn_record: Dict[str, Any]) -> None:
        self.order_history.append(txn_record)

    # New alias to match design/spec
    def add_purchase(self, tx: Dict[str, Any]) -> None:
        self.add_order(tx)

    def get_order_history(self) -> List[Dict[str, Any]]:
        return list(self.order_history)


class FoodItem:
    def __init__(self, name: str, price: float, category: Optional[str] = None, popularity: Optional[float] = None) -> None:
        self.id: str = str(uuid.uuid4())
        self.name = name
        self.price = float(price)
        self.category = category
        self.popularity = float(popularity) if popularity is not None else 0.0
    def update_popularity(self, delta: float) -> None:
        """Adjust popularity by delta (can be negative). Enforce lower bound 0.0."""
        try:
            d = float(delta)
        except Exception:
            raise TypeError("delta must be a number")
        new = (self.popularity or 0.0) + d
        if new < 0.0:
            new = 0.0
        self.popularity = float(new)


class Catalog:
    def __init__(self) -> None:
        # store items by id for correctness; keep a name->id index for backward-compatibility
        self._items: Dict[str, FoodItem] = {}
        self._name_index: Dict[str, str] = {}

    def add_item(self, item: FoodItem) -> None:
        """Add item to catalog. Uses `item.id` as primary key and records a case-insensitive name index."""
        self._items[item.id] = item
        if item.name:
            self._name_index[item.name.lower()] = item.id

    def remove_item(self, item_id: str) -> None:
        """Remove by id or name (case-insensitive)."""
        resolved = self._resolve_id(item_id)
        if not resolved:
            return
        item = self._items.pop(resolved, None)
        if item and item.name:
            self._name_index.pop(item.name.lower(), None)

    def get_item(self, item_id: str) -> Optional[FoodItem]:
        """Get item by id or name (case-insensitive)."""
        resolved = self._resolve_id(item_id)
        if not resolved:
            return None
        return self._items.get(resolved)

    def _resolve_id(self, id_or_name: Optional[str]) -> Optional[str]:
        if not id_or_name:
            return None
        # exact id
        if id_or_name in self._items:
            return id_or_name
        # name lookup (case-insensitive)
        return self._name_index.get(id_or_name.lower())

    def filter_by_category(self, category: str) -> List[FoodItem]:
        if category is None:
            return list(self._items.values())
        cat = category.lower()
        return [it for it in self._items.values() if (it.category or "").lower() == cat]

    def find_item_by_name(self, name: str) -> Optional[FoodItem]:
        if not name:
            return None
        resolved = self._name_index.get(name.lower())
        if not resolved:
            return None
        return self._items.get(resolved)

    def sort_items(self, key: str = "price", reverse: bool = False) -> List[FoodItem]:
        key = (key or "price").lower()
        valid_keys = {"price", "popularity", "name"}
        if key not in valid_keys:
            key = "price"
        if key == "price":
            return sorted(self._items.values(), key=lambda i: (i.price or 0.0), reverse=reverse)
        if key == "popularity":
            return sorted(self._items.values(), key=lambda i: (i.popularity or 0.0), reverse=reverse)
        return sorted(self._items.values(), key=lambda i: (i.name or "").lower(), reverse=reverse)

    def query(self,
              category: Optional[str] = None,
              min_price: Optional[float] = None,
              max_price: Optional[float] = None,
              sort_by: Optional[str] = None,
              reverse: bool = False) -> List[FoodItem]:
        items = list(self._items.values())
        if category is not None:
            items = [i for i in items if (i.category or "").lower() == category.lower()]
        if min_price is not None:
            items = [i for i in items if (i.price or 0.0) >= float(min_price)]
        if max_price is not None:
            items = [i for i in items if (i.price or 0.0) <= float(max_price)]
        if sort_by:
            # sort filtered list directly to avoid extra allocations
            sort_key = (sort_by or "price").lower()
            if sort_key == "price":
                items.sort(key=lambda i: (i.price or 0.0), reverse=reverse)
            elif sort_key == "popularity":
                items.sort(key=lambda i: (i.popularity or 0.0), reverse=reverse)
            else:
                items.sort(key=lambda i: (i.name or "").lower(), reverse=reverse)
            return items
        return items


class Transaction:
    def __init__(self,
                 id: Optional[str],
                 customer_id: str,
                 items: Optional[List[Dict[str, Any]]] = None,
                 total: Optional[float] = None,
                 created_at: Optional[datetime] = None) -> None:
        self.id = id or str(uuid.uuid4())
        self.customer_id = customer_id
        # lines keyed by item id when available; fallback to name-based keys for unknown items
        self._lines: Dict[str, Dict[str, Any]] = {}
        if items:
            for entry in items:
                if isinstance(entry, dict) and "name" in entry and "quantity" in entry and "unit_price" in entry:
                    name = entry["name"]
                    qty = int(entry["quantity"])
                    unit = float(entry["unit_price"])
                    self._add_line(key=name, name=name, unit_price=unit, quantity=qty, item_obj=None)
                elif isinstance(entry, dict) and "item" in entry and "quantity" in entry:
                    itm = entry["item"]
                    qty = int(entry["quantity"])
                    if isinstance(itm, FoodItem):
                        self._add_line(key=itm.id, name=itm.name, unit_price=float(itm.price), quantity=qty, item_obj=itm)
                else:
                    continue
        self.created_at = created_at or datetime.utcnow()
        self.total = float(total) if total is not None else self.compute_total()

    def _add_line(self, key: str, name: str, unit_price: float, quantity: int = 1, item_obj: Optional[FoodItem] = None) -> None:
        if int(quantity) <= 0:
            raise ValueError("quantity must be >= 1")
        if key in self._lines:
            self._lines[key]["quantity"] += int(quantity)
        else:
            self._lines[key] = {"item": item_obj, "name": name, "unit_price": float(unit_price), "quantity": int(quantity)}

    def add_item(self, item: Any, quantity: int = 1) -> None:
        if int(quantity) <= 0:
            raise ValueError("quantity must be >= 1")
        if isinstance(item, FoodItem):
            self._add_line(key=item.id, name=item.name, unit_price=item.price, quantity=quantity, item_obj=item)
        elif isinstance(item, str):
            self._add_line(key=item, name=item, unit_price=0.0, quantity=quantity, item_obj=None)
        elif isinstance(item, dict) and "name" in item and "unit_price" in item:
            self._add_line(key=item.get("id", item["name"]), name=item["name"], unit_price=float(item["unit_price"]), quantity=int(item.get("quantity", 1)), item_obj=item.get("item"))
        else:
            raise ValueError("Unsupported item type for add_item")
        self.total = self.compute_total()

    def remove_item(self, item: Any, quantity: int = 1) -> bool:
        """Remove quantity from a line. Returns True if removed or updated, False if not found."""
        if int(quantity) <= 0:
            raise ValueError("quantity must be >= 1")
        # determine key
        if isinstance(item, FoodItem):
            key = item.id
        elif isinstance(item, str):
            key = item
        elif isinstance(item, dict):
            key = item.get("id") or item.get("name")
        else:
            return False
        if key not in self._lines:
            return False
        self._lines[key]["quantity"] -= int(quantity)
        if self._lines[key]["quantity"] <= 0:
            self._lines.pop(key, None)
        self.total = self.compute_total()
        return True

    def compute_total(self) -> float:
        total = 0.0
        for line in self._lines.values():
            total += float(line.get("unit_price", 0.0)) * int(line.get("quantity", 0))
        return round(total, 2)

    def items_summary(self) -> List[Dict[str, Any]]:
        return [
            {"name": data.get("name"), "item": data.get("item"), "unit_price": data["unit_price"], "quantity": data["quantity"], "line_total": round(data["unit_price"] * data["quantity"], 2)}
            for key, data in self._lines.items()
        ]

    def to_record(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "items": [{"name": data.get("name"), "unit_price": data["unit_price"], "quantity": data["quantity"]} for key, data in self._lines.items()],
            "total": self.total,
            "created_at": self.created_at.isoformat(),
        }
