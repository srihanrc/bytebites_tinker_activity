Mermaid class diagram:

classDiagram

class Customer {
+String name
+ListTransaction purchaseHistory
+bool verifyRealUser()
}

class FoodItem {
+String name
+float price
+String category
+int popularityRating
}

class Catalog {
+ListFoodItem items
+ListFoodItem filterByCategory(String category)
}

class Transaction {
+ListFoodItem items
+float total
+float computeTotal()
}
