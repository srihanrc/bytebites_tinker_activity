"""Scaffold file containing basic class shapes for ByteBites.

These classes are intentionally minimal: constructors and attributes
only, no business logic. They're useful as a starting point for
implementing full behavior later.
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid


class Customer:
    """Basic customer scaffold.

    Attributes:
        id: unique identifier for the customer
        name: customer's full name
        email: contact email
        balance: numeric account balance
        order_history: list of past transaction records
    """

    def __init__(self, name: str, email: str, balance: float = 0.0, id: Optional[str] = None) -> None:
        # generate an id if not supplied
        self.id: str = id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.balance = balance
        self.order_history: List[Dict] = []
        self.verified: bool = False

    def verify_user(self) -> bool:
        """Mark the customer as verified.

        Returns True if the customer was newly verified, False if already verified.
        """
        if getattr(self, "verified", False):
            return False
        self.verified = True
        return True

    def add_order(self, txn_record: Dict) -> None:
        """Append a transaction record to the customer's history."""
        self.order_history.append(txn_record)

    def get_order_history(self) -> List[Dict]:
        """Return the customer's order history (list of transaction records)."""
        return list(self.order_history)


class FoodItem:
    """Basic food item scaffold.

    Attributes:
        id: unique identifier for the item
        name: display name
        price: unit price
        category: optional category label
        popularity: optional numeric popularity rating (e.g. 0.0-5.0)
    """

    def __init__(self, name: str, price: float, category: Optional[str] = None, popularity: Optional[float] = None) -> None:
        self.name = name
        self.price = price
        self.category = category
        self.popularity = popularity


class Catalog:
    """Basic catalog scaffold that stores FoodItem instances.

    Attributes:
        _items: internal mapping of item id -> FoodItem
    """

    def __init__(self) -> None:
        self._items: Dict[str, FoodItem] = {}

    def add_item(self, item: FoodItem) -> None:
        """Add `item` to the catalog (scaffold: no validation)."""
        # use item name as the key for this simple scaffold
        self._items[item.name] = item

    def remove_item(self, item_id: str) -> None:
        """Remove `item_id` from the catalog (scaffold)."""
        # item_id is the key (name) in this scaffold
        self._items.pop(item_id, None)

    def get_item(self, item_id: str) -> Optional[FoodItem]:
        """Return the item or None (scaffold)."""
        return self._items.get(item_id)


class Transaction:
    """Basic transaction scaffold.

    Attributes:
        id: unique transaction id
        customer_id: id of purchasing customer
        items: list of dicts with item references and quantities
        total: numeric total amount
        created_at: timestamp
    """

    def __init__(self, id: str, customer_id: str, items: List[Dict], total: float, created_at: Optional[datetime] = None) -> None:
        self.id = id
        self.customer_id = customer_id
        self.items = items
        self.total = total
        self.created_at = created_at or datetime.utcnow()

    def to_record(self) -> Dict:
        """Return a serializable record of the transaction (scaffold)."""
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "items": self.items,
            "total": self.total,
            "created_at": self.created_at.isoformat(),
        }
