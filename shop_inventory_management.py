import json
import datetime
from typing import List, Dict, Optional
import os

class Product:
    """Class to represent a product in the inventory"""
    
    def __init__(self, product_id: str, name: str, price: float, quantity: int, category: str = "General"):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        self.min_stock_threshold = 10  # Alert when stock falls below this
    
    def to_dict(self) -> Dict:
        """Convert product to dictionary for JSON serialization"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'category': self.category,
            'min_stock_threshold': self.min_stock_threshold
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Product':
        """Create product from dictionary"""
        product = cls(
            data['product_id'],
            data['name'],
            data['price'],
            data['quantity'],
            data.get('category', 'General')
        )
        product.min_stock_threshold = data.get('min_stock_threshold', 10)
        return product
    
    def __str__(self):
        return f"ID: {self.product_id}, Name: {self.name}, Price: Rs{self.price:.2f}, Stock: {self.quantity}, Category: {self.category}"

class Inventory:
    """Class to manage the shop inventory"""
    
    def __init__(self, inventory_file: str = "inventory.json"):
        self.inventory_file = inventory_file
        self.products: Dict[str, Product] = {}
        self.load_inventory()
    
    def load_inventory(self):
        """Load inventory from JSON file"""
        if os.path.exists(self.inventory_file):
            try:
                with open(self.inventory_file, 'r') as f:
                    data = json.load(f)
                    for product_data in data:
                        product = Product.from_dict(product_data)
                        self.products[product.product_id] = product
                print(f"Inventory loaded successfully. {len(self.products)} products found.")
            except Exception as e:
                print(f"Error loading inventory: {e}")
                self.products = {}
        else:
            print("No existing inventory file found. Starting with empty inventory.")
    
    def save_inventory(self):
        """Save inventory to JSON file"""
        try:
            data = [product.to_dict() for product in self.products.values()]
            with open(self.inventory_file, 'w') as f:
                json.dump(data, f, indent=2)
            print("Inventory saved successfully.")
        except Exception as e:
            print(f"Error saving inventory: {e}")
    
    def add_product(self, product_id: str, name: str, price: float, quantity: int, category: str = "General"):
        """Add a new product to inventory"""
        if product_id in self.products:
            print(f"Product with ID {product_id} already exists. Use update_product to modify.")
            return False
        
        product = Product(product_id, name, price, quantity, category)
        self.products[product_id] = product
        self.save_inventory()
        print(f"Product '{name}' added successfully.")
        return True
    
    def update_product(self, product_id: str, **kwargs):
        """Update product information"""
        if product_id not in self.products:
            print(f"Product with ID {product_id} not found.")
            return False
        
        product = self.products[product_id]
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        self.save_inventory()
        print(f"Product {product_id} updated successfully.")
        return True
    
    def remove_product(self, product_id: str):
        """Remove product from inventory"""
        if product_id not in self.products:
            print(f"Product with ID {product_id} not found.")
            return False
        
        product_name = self.products[product_id].name
        del self.products[product_id]
        self.save_inventory()
        print(f"Product '{product_name}' removed successfully.")
        return True
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        return self.products.get(product_id)
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or category"""
        query = query.lower()
        results = []
        for product in self.products.values():
            if (query in product.name.lower() or 
                query in product.category.lower() or 
                query in product.product_id.lower()):
                results.append(product)
        return results
    
    def get_low_stock_products(self) -> List[Product]:
        """Get products with stock below threshold"""
        low_stock = []
        for product in self.products.values():
            if product.quantity <= product.min_stock_threshold:
                low_stock.append(product)
        return low_stock
    
    def update_stock(self, product_id: str, quantity_change: int):
        """Update product stock (positive for adding, negative for removing)"""
        if product_id not in self.products:
            print(f"Product with ID {product_id} not found.")
            return False
        
        product = self.products[product_id]
        new_quantity = product.quantity + quantity_change
        
        if new_quantity < 0:
            print(f"Insufficient stock. Available: {product.quantity}, Requested: {abs(quantity_change)}")
            return False
        
        product.quantity = new_quantity
        self.save_inventory()
        
        # Check for low stock alert
        if product.quantity <= product.min_stock_threshold:
            self.generate_low_stock_alert(product)
        
        return True
    
    def generate_low_stock_alert(self, product: Product):
        """Generate alert for low stock"""
        alert_message = f"*** LOW STOCK ALERT ***\n"
        alert_message += f"Product: {product.name} (ID: {product.product_id})\n"
        alert_message += f"Current Stock: {product.quantity}\n"
        alert_message += f"Minimum Threshold: {product.min_stock_threshold}\n"
        alert_message += f"Please restock this item immediately!\n"
        alert_message += "=" * 50
        
        print(alert_message)
        
        # Save alert to file
        with open("low_stock_alerts.txt", "a") as f:
            f.write(f"\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(alert_message)
            f.write("\n")

class Billing:
    """Class to handle billing and sales transactions"""
    
    def __init__(self, inventory: Inventory, sales_file: str = "sales.json"):
        self.inventory = inventory
        self.sales_file = sales_file
        self.current_transaction = []
        self.load_sales_history()
    
    def load_sales_history(self):
        """Load sales history from JSON file"""
        if os.path.exists(self.sales_file):
            try:
                with open(self.sales_file, 'r') as f:
                    self.sales_history = json.load(f)
            except Exception as e:
                print(f"Error loading sales history: {e}")
                self.sales_history = []
        else:
            self.sales_history = []
    
    def save_sales_history(self):
        """Save sales history to JSON file"""
        try:
            with open(self.sales_file, 'w') as f:
                json.dump(self.sales_history, f, indent=2)
        except Exception as e:
            print(f"Error saving sales history: {e}")
    
    def add_to_cart(self, product_id: str, quantity: int):
        """Add product to current transaction"""
        product = self.inventory.get_product(product_id)
        if not product:
            print(f"Product with ID {product_id} not found.")
            return False
        
        if product.quantity < quantity:
            print(f"Insufficient stock. Available: {product.quantity}, Requested: {quantity}")
            return False
        
        # Check if product already in cart
        for item in self.current_transaction:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                print(f"Updated quantity for {product.name} in cart.")
                return True
        
        # Add new item to cart
        self.current_transaction.append({
            'product_id': product_id,
            'name': product.name,
            'price': product.price,
            'quantity': quantity,
            'total': product.price * quantity
        })
        
        print(f"Added {quantity} x {product.name} to cart.")
        return True
    
    def remove_from_cart(self, product_id: str, quantity: int = None):
        """Remove product from current transaction"""
        for i, item in enumerate(self.current_transaction):
            if item['product_id'] == product_id:
                if quantity is None or quantity >= item['quantity']:
                    # Remove entire item
                    removed_item = self.current_transaction.pop(i)
                    print(f"Removed {removed_item['name']} from cart.")
                else:
                    # Reduce quantity
                    item['quantity'] -= quantity
                    item['total'] = item['price'] * item['quantity']
                    print(f"Reduced quantity of {item['name']} by {quantity}.")
                return True
        
        print(f"Product with ID {product_id} not found in cart.")
        return False
    
    def view_cart(self):
        """Display current transaction items"""
        if not self.current_transaction:
            print("Cart is empty.")
            return
        
        print("\n" + "="*60)
        print("CURRENT CART")
        print("="*60)
        print(f"{'Product':<20} {'Price':<10} {'Qty':<5} {'Total':<10}")
        print("-"*60)
        
        total_amount = 0
        for item in self.current_transaction:
            print(f"{item['name']:<20} Rs{item['price']:<9.2f} {item['quantity']:<5} Rs{item['total']:<9.2f}")
            total_amount += item['total']
        
        print("-"*60)
        print(f"{'TOTAL AMOUNT':<35} Rs{total_amount:.2f}")
        print("="*60)
    
    def process_payment(self, payment_amount: float, customer_name: str = "Walk-in Customer"):
        """Process payment and complete transaction"""
        if not self.current_transaction:
            print("No items in cart to process.")
            return False
        
        # Calculate total
        total_amount = sum(item['total'] for item in self.current_transaction)
        
        if payment_amount < total_amount:
            print(f"Insufficient payment. Total: Rs{total_amount:.2f}, Paid: Rs{payment_amount:.2f}")
            return False
        
        # Generate transaction ID
        transaction_id = f"TXN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create transaction record
        transaction = {
            'transaction_id': transaction_id,
            'customer_name': customer_name,
            'timestamp': datetime.datetime.now().isoformat(),
            'items': self.current_transaction.copy(),
            'total_amount': total_amount,
            'payment_amount': payment_amount,
            'change': payment_amount - total_amount
        }
        
        # Update inventory
        for item in self.current_transaction:
            self.inventory.update_stock(item['product_id'], -item['quantity'])
        
        # Save transaction
        self.sales_history.append(transaction)
        self.save_sales_history()
        
        # Generate receipt
        self.generate_receipt(transaction)
        
        # Clear current transaction
        self.current_transaction.clear()
        
        print(f"Transaction completed successfully! Transaction ID: {transaction_id}")
        return True
    
    def generate_receipt(self, transaction: Dict):
        """Generate and display receipt"""
        print("\n" + "="*60)
        print("RECEIPT")
        print("="*60)
        print(f"Transaction ID: {transaction['transaction_id']}")
        print(f"Customer: {transaction['customer_name']}")
        print(f"Date: {datetime.datetime.fromisoformat(transaction['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*60)
        print(f"{'Product':<20} {'Price':<10} {'Qty':<5} {'Total':<10}")
        print("-"*60)
        
        for item in transaction['items']:
            print(f"{item['name']:<20} Rs{item['price']:<9.2f} {item['quantity']:<5} Rs{item['total']:<9.2f}")
        
        print("-"*60)
        print(f"{'TOTAL AMOUNT':<35} Rs{transaction['total_amount']:.2f}")
        print(f"{'PAID AMOUNT':<35} Rs{transaction['payment_amount']:.2f}")
        print(f"{'CHANGE':<35} Rs{transaction['change']:.2f}")
        print("="*60)
        print("Thank you for your business!")
        print("="*60)
    
    def get_sales_summary(self, date_from: str = None, date_to: str = None):
        """Get sales summary for a date range"""
        if not self.sales_history:
            print("No sales history found.")
            return
        
        filtered_sales = self.sales_history
        
        if date_from:
            filtered_sales = [s for s in filtered_sales if s['timestamp'] >= date_from]
        
        if date_to:
            filtered_sales = [s for s in filtered_sales if s['timestamp'] <= date_to]
        
        total_sales = sum(s['total_amount'] for s in filtered_sales)
        total_transactions = len(filtered_sales)
        
        print(f"\nSALES SUMMARY")
        print(f"Period: {date_from or 'All time'} to {date_to or 'Present'}")
        print(f"Total Transactions: {total_transactions}")
        print(f"Total Sales: Rs{total_sales:.2f}")
        print(f"Average Transaction: Rs{total_sales/total_transactions:.2f}" if total_transactions > 0 else "No transactions")

class ShopInventoryManager:
    """Main application class"""
    
    def __init__(self):
        self.inventory = Inventory()
        self.billing = Billing(self.inventory)
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("SHOP INVENTORY MANAGEMENT SYSTEM")
        print("="*60)
        print("1. Inventory Management")
        print("2. Billing System")
        print("3. View Low Stock Alerts")
        print("4. Sales Reports")
        print("5. Exit")
        print("="*60)
    
    def inventory_menu(self):
        """Display inventory management menu"""
        while True:
            print("\n" + "="*40)
            print("INVENTORY MANAGEMENT")
            print("="*40)
            print("1. Add Product")
            print("2. Update Product")
            print("3. Remove Product")
            print("4. View All Products")
            print("5. Search Products")
            print("6. Update Stock")
            print("7. Back to Main Menu")
            print("="*40)
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.update_product()
            elif choice == '3':
                self.remove_product()
            elif choice == '4':
                self.view_all_products()
            elif choice == '5':
                self.search_products()
            elif choice == '6':
                self.update_stock()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def billing_menu(self):
        """Display billing menu"""
        while True:
            print("\n" + "="*40)
            print("BILLING SYSTEM")
            print("="*40)
            print("1. Add to Cart")
            print("2. Remove from Cart")
            print("3. View Cart")
            print("4. Process Payment")
            print("5. Clear Cart")
            print("6. Back to Main Menu")
            print("="*40)
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.add_to_cart()
            elif choice == '2':
                self.remove_from_cart()
            elif choice == '3':
                self.billing.view_cart()
            elif choice == '4':
                self.process_payment()
            elif choice == '5':
                self.billing.current_transaction.clear()
                print("Cart cleared.")
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def add_product(self):
        """Add new product"""
        print("\n--- ADD NEW PRODUCT ---")
        product_id = input("Enter Product ID: ").strip()
        name = input("Enter Product Name: ").strip()
        
        try:
            price = float(input("Enter Price: "))
            quantity = int(input("Enter Initial Quantity: "))
            category = input("Enter Category (optional): ").strip() or "General"
            
            self.inventory.add_product(product_id, name, price, quantity, category)
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
    
    def update_product(self):
        """Update existing product"""
        print("\n--- UPDATE PRODUCT ---")
        product_id = input("Enter Product ID: ").strip()
        
        if not self.inventory.get_product(product_id):
            print("Product not found.")
            return
        
        print("Enter new values (press Enter to keep current value):")
        name = input("Name: ").strip()
        price = input("Price: ").strip()
        quantity = input("Quantity: ").strip()
        category = input("Category: ").strip()
        
        updates = {}
        if name:
            updates['name'] = name
        if price:
            try:
                updates['price'] = float(price)
            except ValueError:
                print("Invalid price format.")
                return
        if quantity:
            try:
                updates['quantity'] = int(quantity)
            except ValueError:
                print("Invalid quantity format.")
                return
        if category:
            updates['category'] = category
        
        if updates:
            self.inventory.update_product(product_id, **updates)
        else:
            print("No updates provided.")
    
    def remove_product(self):
        """Remove product"""
        print("\n--- REMOVE PRODUCT ---")
        product_id = input("Enter Product ID: ").strip()
        confirm = input(f"Are you sure you want to remove this product? (y/n): ").strip().lower()
        
        if confirm == 'y':
            self.inventory.remove_product(product_id)
        else:
            print("Operation cancelled.")
    
    def view_all_products(self):
        """View all products"""
        print("\n--- ALL PRODUCTS ---")
        if not self.inventory.products:
            print("No products found.")
            return
        
        print(f"{'ID':<10} {'Name':<20} {'Price':<10} {'Stock':<8} {'Category':<15}")
        print("-" * 70)
        
        for product in self.inventory.products.values():
            print(f"{product.product_id:<10} {product.name:<20} Rs{product.price:<9.2f} {product.quantity:<8} {product.category:<15}")
    
    def search_products(self):
        """Search products"""
        print("\n--- SEARCH PRODUCTS ---")
        query = input("Enter search term (name, category, or ID): ").strip()
        
        results = self.inventory.search_products(query)
        
        if not results:
            print("No products found matching your search.")
            return
        
        print(f"\nFound {len(results)} product(s):")
        print(f"{'ID':<10} {'Name':<20} {'Price':<10} {'Stock':<8} {'Category':<15}")
        print("-" * 70)
        
        for product in results:
            print(f"{product.product_id:<10} {product.name:<20} Rs{product.price:<9.2f} {product.quantity:<8} {product.category:<15}")
    
    def update_stock(self):
        """Update product stock"""
        print("\n--- UPDATE STOCK ---")
        product_id = input("Enter Product ID: ").strip()
        
        product = self.inventory.get_product(product_id)
        if not product:
            print("Product not found.")
            return
        
        print(f"Current stock for {product.name}: {product.quantity}")
        
        try:
            change = int(input("Enter quantity change (+ to add, - to remove): "))
            self.inventory.update_stock(product_id, change)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    def add_to_cart(self):
        """Add product to cart"""
        print("\n--- ADD TO CART ---")
        product_id = input("Enter Product ID: ").strip()
        
        product = self.inventory.get_product(product_id)
        if not product:
            print("Product not found.")
            return
        
        print(f"Product: {product.name}")
        print(f"Price: Rs{product.price:.2f}")
        print(f"Available Stock: {product.quantity}")
        
        try:
            quantity = int(input("Enter quantity: "))
            self.billing.add_to_cart(product_id, quantity)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    def remove_from_cart(self):
        """Remove product from cart"""
        print("\n--- REMOVE FROM CART ---")
        product_id = input("Enter Product ID: ").strip()
        
        try:
            quantity = input("Enter quantity to remove (or press Enter to remove all): ").strip()
            quantity = int(quantity) if quantity else None
            self.billing.remove_from_cart(product_id, quantity)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    def process_payment(self):
        """Process payment"""
        if not self.billing.current_transaction:
            print("Cart is empty. Add items before processing payment.")
            return
        
        self.billing.view_cart()
        
        customer_name = input("Enter customer name (or press Enter for 'Walk-in Customer'): ").strip()
        if not customer_name:
            customer_name = "Walk-in Customer"
        
        try:
            payment_amount = float(input("Enter payment amount: "))
            self.billing.process_payment(payment_amount, customer_name)
        except ValueError:
            print("Invalid input. Please enter a valid amount.")
    
    def view_low_stock_alerts(self):
        """View low stock alerts"""
        print("\n--- LOW STOCK ALERTS ---")
        low_stock_products = self.inventory.get_low_stock_products()
        
        if not low_stock_products:
            print("No low stock alerts. All products are well stocked!")
            return
        
        print(f"Found {len(low_stock_products)} product(s) with low stock:")
        print(f"{'ID':<10} {'Name':<20} {'Current Stock':<15} {'Threshold':<10}")
        print("-" * 60)
        
        for product in low_stock_products:
            print(f"{product.product_id:<10} {product.name:<20} {product.quantity:<15} {product.min_stock_threshold:<10}")
    
    def sales_reports_menu(self):
        """Display sales reports menu"""
        while True:
            print("\n" + "="*40)
            print("SALES REPORTS")
            print("="*40)
            print("1. Sales Summary")
            print("2. View All Transactions")
            print("3. Back to Main Menu")
            print("="*40)
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                self.billing.get_sales_summary()
            elif choice == '2':
                self.view_all_transactions()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def view_all_transactions(self):
        """View all transactions"""
        print("\n--- ALL TRANSACTIONS ---")
        if not self.billing.sales_history:
            print("No transactions found.")
            return
        
        print(f"{'Transaction ID':<20} {'Customer':<20} {'Amount':<10} {'Date':<15}")
        print("-" * 70)
        
        for transaction in self.billing.sales_history:
            date = datetime.datetime.fromisoformat(transaction['timestamp']).strftime('%Y-%m-%d')
            print(f"{transaction['transaction_id']:<20} {transaction['customer_name']:<20} Rs{transaction['total_amount']:<9.2f} {date:<15}")
    
    def run(self):
        """Main application loop"""
        print("Welcome to Shop Inventory Management System!")
        print("Loading system...")
        
        # Check for low stock alerts on startup
        low_stock_products = self.inventory.get_low_stock_products()
        if low_stock_products:
            print(f"\n*** ATTENTION: {len(low_stock_products)} product(s) have low stock! ***")
            for product in low_stock_products:
                print(f"   - {product.name} (ID: {product.product_id}): {product.quantity} units")
        
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                self.inventory_menu()
            elif choice == '2':
                self.billing_menu()
            elif choice == '3':
                self.view_low_stock_alerts()
            elif choice == '4':
                self.sales_reports_menu()
            elif choice == '5':
                print("Thank you for using Shop Inventory Management System!")
                break
            else:
                print("Invalid choice. Please try again.")

def create_demo_data():
    """Create demo data for testing"""
    inventory = Inventory()
    
    # Add some demo products
    demo_products = [
        ("P001", "Laptop", 45000.00, 15, "Electronics"),
        ("P002", "Mouse", 500.00, 8, "Electronics"),
        ("P003", "Keyboard", 1200.00, 5, "Electronics"),
        ("P004", "Notebook", 50.00, 25, "Stationery"),
        ("P005", "Pen", 10.00, 3, "Stationery"),
        ("P006", "Coffee Mug", 200.00, 12, "Kitchen"),
        ("P007", "Water Bottle", 300.00, 7, "Kitchen"),
        ("P008", "T-Shirt", 500.00, 20, "Clothing"),
        ("P009", "Jeans", 1500.00, 4, "Clothing"),
        ("P010", "Shoes", 2500.00, 6, "Clothing")
    ]
    
    print("Creating demo data...")
    for product_data in demo_products:
        inventory.add_product(*product_data)
    
    print("Demo data created successfully!")
    print("Note: Some products have low stock to demonstrate the alert system.")

if __name__ == "__main__":
    # Create demo data if inventory is empty
    temp_inventory = Inventory()
    if not temp_inventory.products:
        create_demo_data()
    
    # Start the application
    app = ShopInventoryManager()
    app.run()
