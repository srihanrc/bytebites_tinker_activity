# ByteBites Design — UML Class Diagram

This file contains a revised UML class diagram for the core backend classes.

```mermaid
classDiagram
    class Customer {
      +String name
      +List~Transaction~ purchaseHistory
      +bool isVerified
      +verifyIdentity(): bool
      +addPurchase(tx: Transaction): void
    }

    class FoodItem {
      +String name
      +float price
      +String category
      +int popularityRating
      +updatePopularity(delta: int): void
    }

    class Catalog {
      +List~FoodItem~ items
      +addItem(item: FoodItem): void
      +removeItem(itemId: String): void
      +filterByCategory(category: String): List~FoodItem~
      +findItemByName(name: String): FoodItem
    }

    class Transaction {
      +List~FoodItem~ items
      +float totalCost
      +computeTotal(): float
      +addItem(item: FoodItem): void
      +removeItem(item: FoodItem): void
    }

    Catalog "1" o-- "*" FoodItem : contains
    Transaction "1" o-- "*" FoodItem : includes
    Customer "1" o-- "*" Transaction : purchases

```

Notes:
- `Customer` stores name and a list of past `Transaction`s and can verify identity.
- `FoodItem` holds item details: name, price, category, and popularity rating.
- `Catalog` manages a collection of `FoodItem`s and supports filtering by category.
- `Transaction` groups selected `FoodItem`s and computes the total cost.
