import streamlit as st
import json
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Optional
import os

# Page configuration
st.set_page_config(
    page_title="Jain General & Stationery Store Management System",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
    .success-card {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .error-card {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

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
            except Exception as e:
                st.error(f"Error loading inventory: {e}")
                self.products = {}
    
    def save_inventory(self):
        """Save inventory to JSON file"""
        try:
            data = [product.to_dict() for product in self.products.values()]
            with open(self.inventory_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving inventory: {e}")
            return False
    
    def add_product(self, product_id: str, name: str, price: float, quantity: int, category: str = "General"):
        """Add a new product to inventory"""
        if product_id in self.products:
            return False, f"Product with ID {product_id} already exists."
        
        product = Product(product_id, name, price, quantity, category)
        self.products[product_id] = product
        if self.save_inventory():
            return True, f"Product '{name}' added successfully."
        return False, "Error saving product."
    
    def update_product(self, product_id: str, **kwargs):
        """Update product information"""
        if product_id not in self.products:
            return False, f"Product with ID {product_id} not found."
        
        product = self.products[product_id]
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        if self.save_inventory():
            return True, f"Product {product_id} updated successfully."
        return False, "Error saving changes."
    
    def remove_product(self, product_id: str):
        """Remove product from inventory"""
        if product_id not in self.products:
            return False, f"Product with ID {product_id} not found."
        
        product_name = self.products[product_id].name
        del self.products[product_id]
        if self.save_inventory():
            return True, f"Product '{product_name}' removed successfully."
        return False, "Error saving changes."
    
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
            return False, f"Product with ID {product_id} not found."
        
        product = self.products[product_id]
        new_quantity = product.quantity + quantity_change
        
        if new_quantity < 0:
            return False, f"Insufficient stock. Available: {product.quantity}, Requested: {abs(quantity_change)}"
        
        product.quantity = new_quantity
        if self.save_inventory():
            return True, f"Stock updated successfully. New quantity: {new_quantity}"
        return False, "Error saving changes."

class Billing:
    """Class to handle billing and sales transactions"""
    
    def __init__(self, inventory: Inventory, sales_file: str = "sales.json"):
        self.inventory = inventory
        self.sales_file = sales_file
        self.load_sales_history()
    
    def load_sales_history(self):
        """Load sales history from JSON file"""
        if os.path.exists(self.sales_file):
            try:
                with open(self.sales_file, 'r') as f:
                    self.sales_history = json.load(f)
            except Exception as e:
                st.error(f"Error loading sales history: {e}")
                self.sales_history = []
        else:
            self.sales_history = []
    
    def save_sales_history(self):
        """Save sales history to JSON file"""
        try:
            with open(self.sales_file, 'w') as f:
                json.dump(self.sales_history, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving sales history: {e}")
            return False
    
    def process_payment(self, cart_items: List[Dict], payment_amount: float, customer_name: str = "Walk-in Customer"):
        """Process payment and complete transaction"""
        if not cart_items:
            return False, "No items in cart to process."
        
        # Calculate total
        total_amount = sum(item['total'] for item in cart_items)
        
        if payment_amount < total_amount:
            return False, f"Insufficient payment. Total: Rs{total_amount:.2f}, Paid: Rs{payment_amount:.2f}"
        
        # Generate transaction ID
        transaction_id = f"TXN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create transaction record
        transaction = {
            'transaction_id': transaction_id,
            'customer_name': customer_name,
            'timestamp': datetime.datetime.now().isoformat(),
            'items': cart_items.copy(),
            'total_amount': total_amount,
            'payment_amount': payment_amount,
            'change': payment_amount - total_amount
        }
        
        # Update inventory
        for item in cart_items:
            success, message = self.inventory.update_stock(item['product_id'], -item['quantity'])
            if not success:
                return False, f"Error updating stock for {item['name']}: {message}"
        
        # Save transaction
        self.sales_history.append(transaction)
        if self.save_sales_history():
            return True, transaction
        return False, "Error saving transaction."

# Initialize session state
if 'inventory' not in st.session_state:
    st.session_state.inventory = Inventory()
if 'billing' not in st.session_state:
    st.session_state.billing = Billing(st.session_state.inventory)
if 'cart' not in st.session_state:
    st.session_state.cart = []

def create_demo_data():
    """Create demo data for testing"""
    inventory = st.session_state.inventory
    
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
    
    for product_data in demo_products:
        inventory.add_product(*product_data)

# Create demo data if inventory is empty
if not st.session_state.inventory.products:
    create_demo_data()

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🏪 Shop Inventory Management System</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Dashboard", "Inventory Management", "Billing System", "Low Stock Alerts", "Sales Reports", "Error Monitor"]
    )
    
    # Dashboard page
    if page == "Dashboard":
        show_dashboard()
    
    # Inventory Management page
    elif page == "Inventory Management":
        show_inventory_management()
    
    # Billing System page
    elif page == "Billing System":
        show_billing_system()
    
    # Low Stock Alerts page
    elif page == "Low Stock Alerts":
        show_low_stock_alerts()
    
    # Sales Reports page
    elif page == "Sales Reports":
        show_sales_reports()
    
    # Error Monitor page
    elif page == "Error Monitor":
        show_error_monitor()

def show_dashboard():
    """Display the main dashboard"""
    st.header("📊 Dashboard Overview")
    
    inventory = st.session_state.inventory
    billing = st.session_state.billing
    
    # Error handling and system status
    try:
        # Check for system errors
        error_messages = []
        
        # Check inventory file accessibility
        if not os.path.exists("inventory.json"):
            error_messages.append("⚠️ Inventory file not found - using empty inventory")
        
        # Check sales file accessibility
        if not os.path.exists("sales.json"):
            error_messages.append("⚠️ Sales file not found - starting with empty sales history")
        
        # Check for low stock products
        low_stock_products = inventory.get_low_stock_products()
        if low_stock_products:
            error_messages.append(f"🚨 {len(low_stock_products)} products have low stock!")
        
        # Display errors prominently
        if error_messages:
            st.error("**SYSTEM ALERTS:**")
            for error in error_messages:
                st.error(error)
            st.markdown("---")
        
        # System status indicator
        col_status1, col_status2, col_status3 = st.columns(3)
        
        with col_status1:
            if inventory.products:
                st.success("✅ Inventory System: Active")
            else:
                st.warning("⚠️ Inventory System: Empty")
        
        with col_status2:
            if billing.sales_history:
                st.success("✅ Sales System: Active")
            else:
                st.info("ℹ️ Sales System: No transactions yet")
        
        with col_status3:
            if low_stock_products:
                st.error(f"🚨 Low Stock Alert: {len(low_stock_products)} items")
            else:
                st.success("✅ Stock Levels: All Good")
        
        st.markdown("---")
        
    except Exception as e:
        st.error(f"**SYSTEM ERROR:** {str(e)}")
        st.error("Please check the system configuration and try again.")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Products",
            value=len(inventory.products),
            delta=None
        )
    
    with col2:
        total_value = sum(product.price * product.quantity for product in inventory.products.values())
        st.metric(
            label="Total Inventory Value",
            value=f"Rs{total_value:,.2f}",
            delta=None
        )
    
    with col3:
        low_stock_count = len(inventory.get_low_stock_products())
        st.metric(
            label="Low Stock Items",
            value=low_stock_count,
            delta=None
        )
    
    with col4:
        total_sales = sum(transaction['total_amount'] for transaction in billing.sales_history)
        st.metric(
            label="Total Sales",
            value=f"Rs{total_sales:,.2f}",
            delta=None
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Inventory by Category")
        if inventory.products:
            category_data = {}
            for product in inventory.products.values():
                category_data[product.category] = category_data.get(product.category, 0) + product.quantity
            
            fig = px.pie(
                values=list(category_data.values()),
                names=list(category_data.keys()),
                title="Stock Distribution by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Stock Levels")
        if inventory.products:
            products_data = []
            for product in inventory.products.values():
                products_data.append({
                    'Product': product.name,
                    'Stock': product.quantity,
                    'Category': product.category,
                    'Low Stock': product.quantity <= product.min_stock_threshold
                })
            
            df = pd.DataFrame(products_data)
            fig = px.bar(
                df,
                x='Product',
                y='Stock',
                color='Low Stock',
                title="Current Stock Levels",
                color_discrete_map={True: 'red', False: 'green'}
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # System Health Check
    st.subheader("🔍 System Health Check")
    
    health_col1, health_col2, health_col3 = st.columns(3)
    
    with health_col1:
        # Check file permissions
        try:
            with open("inventory.json", "r") as f:
                json.load(f)
            st.success("✅ Inventory File: Readable")
        except Exception as e:
            st.error(f"❌ Inventory File Error: {str(e)}")
    
    with health_col2:
        # Check sales file
        try:
            with open("sales.json", "r") as f:
                json.load(f)
            st.success("✅ Sales File: Readable")
        except Exception as e:
            st.error(f"❌ Sales File Error: {str(e)}")
    
    with health_col3:
        # Check data integrity
        try:
            total_products = len(inventory.products)
            total_sales = len(billing.sales_history)
            st.success(f"✅ Data Integrity: {total_products} products, {total_sales} sales")
        except Exception as e:
            st.error(f"❌ Data Integrity Error: {str(e)}")
    
    # Error Log Section
    st.subheader("📋 System Error Log")
    
    # Check for common errors
    error_log = []
    
    # Check for products with invalid data
    for product_id, product in inventory.products.items():
        if product.price < 0:
            error_log.append(f"❌ Product {product_id}: Negative price (Rs{product.price})")
        if product.quantity < 0:
            error_log.append(f"❌ Product {product_id}: Negative quantity ({product.quantity})")
        if not product.name.strip():
            error_log.append(f"❌ Product {product_id}: Empty name")
    
    # Check for sales with invalid data
    for transaction in billing.sales_history:
        if transaction['total_amount'] < 0:
            error_log.append(f"❌ Transaction {transaction['transaction_id']}: Negative total amount")
        if transaction['payment_amount'] < transaction['total_amount']:
            error_log.append(f"❌ Transaction {transaction['transaction_id']}: Insufficient payment")
    
    if error_log:
        st.error("**DETECTED ERRORS:**")
        for error in error_log[:10]:  # Show first 10 errors
            st.error(error)
        if len(error_log) > 10:
            st.warning(f"... and {len(error_log) - 10} more errors")
    else:
        st.success("✅ No system errors detected")
    
    st.markdown("---")
    
    # Recent transactions
    st.subheader("🔄 Recent Transactions")
    if billing.sales_history:
        recent_transactions = billing.sales_history[-5:]  # Last 5 transactions
        for transaction in reversed(recent_transactions):
            with st.expander(f"Transaction {transaction['transaction_id']} - {transaction['customer_name']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Date:** {datetime.datetime.fromisoformat(transaction['timestamp']).strftime('%Y-%m-%d %H:%M')}")
                with col2:
                    st.write(f"**Total:** Rs{transaction['total_amount']:.2f}")
                with col3:
                    st.write(f"**Items:** {len(transaction['items'])}")
                
                # Show items
                for item in transaction['items']:
                    st.write(f"- {item['name']} x{item['quantity']} = Rs{item['total']:.2f}")
    else:
        st.info("No transactions yet.")

def show_inventory_management():
    """Display inventory management interface"""
    st.header("📦 Inventory Management")
    
    inventory = st.session_state.inventory
    
    # Tabs for different operations
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["View Products", "Add Product", "Update Product", "Update Stock", "Remove Product"])
    
    with tab1:
        st.subheader("📋 All Products")
        
        # Search functionality
        search_query = st.text_input("🔍 Search products", placeholder="Search by name, category, or ID")
        
        if search_query:
            products = inventory.search_products(search_query)
        else:
            products = list(inventory.products.values())
        
        if products:
            # Convert to DataFrame for better display
            products_data = []
            for product in products:
                products_data.append({
                    'ID': product.product_id,
                    'Name': product.name,
                    'Price': f"Rs{product.price:.2f}",
                    'Stock': product.quantity,
                    'Category': product.category,
                    'Low Stock': '⚠️ Yes' if product.quantity <= product.min_stock_threshold else '✅ No'
                })
            
            df = pd.DataFrame(products_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No products found.")
    
    with tab2:
        st.subheader("➕ Add New Product")
        
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                product_id = st.text_input("Product ID", placeholder="e.g., P001")
                name = st.text_input("Product Name", placeholder="e.g., Laptop")
                price = st.number_input("Price (Rs)", min_value=0.0, step=0.01)
            
            with col2:
                quantity = st.number_input("Initial Quantity", min_value=0, step=1)
                category = st.selectbox("Category", ["Electronics", "Stationery", "Kitchen", "Clothing", "General"])
            
            submitted = st.form_submit_button("Add Product")
            
            if submitted:
                if product_id and name and price > 0:
                    success, message = inventory.add_product(product_id, name, price, quantity, category)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all required fields.")
    
    with tab3:
        st.subheader("✏️ Update Product")
        
        if inventory.products:
            product_id = st.selectbox("Select Product to Update", list(inventory.products.keys()))
            
            if product_id:
                product = inventory.get_product(product_id)
                
                with st.form("update_product_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("Name", value=product.name)
                        new_price = st.number_input("Price (Rs)", value=product.price, min_value=0.0, step=0.01)
                    
                    with col2:
                        new_quantity = st.number_input("Quantity", value=product.quantity, min_value=0, step=1)
                        new_category = st.selectbox("Category", ["Electronics", "Stationery", "Kitchen", "Clothing", "General"], 
                                                   index=["Electronics", "Stationery", "Kitchen", "Clothing", "General"].index(product.category))
                    
                    submitted = st.form_submit_button("Update Product")
                    
                    if submitted:
                        success, message = inventory.update_product(
                            product_id,
                            name=new_name,
                            price=new_price,
                            quantity=new_quantity,
                            category=new_category
                        )
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("No products to update.")
    
    with tab4:
        st.subheader("📊 Update Stock")
        
        if inventory.products:
            product_id = st.selectbox("Select Product", list(inventory.products.keys()))
            
            if product_id:
                product = inventory.get_product(product_id)
                st.write(f"**Current Stock:** {product.quantity}")
                
                with st.form("update_stock_form"):
                    change_type = st.radio("Change Type", ["Add Stock", "Remove Stock"])
                    quantity_change = st.number_input("Quantity Change", min_value=1, step=1)
                    
                    if change_type == "Remove Stock":
                        quantity_change = -quantity_change
                    
                    submitted = st.form_submit_button("Update Stock")
                    
                    if submitted:
                        success, message = inventory.update_stock(product_id, quantity_change)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("No products to update.")
    
    with tab5:
        st.subheader("🗑️ Remove Product")
        
        if inventory.products:
            product_id = st.selectbox("Select Product to Remove", list(inventory.products.keys()))
            
            if product_id:
                product = inventory.get_product(product_id)
                st.write(f"**Product:** {product.name}")
                st.write(f"**Current Stock:** {product.quantity}")
                
                if st.button("Remove Product", type="primary"):
                    success, message = inventory.remove_product(product_id)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.info("No products to remove.")

def show_billing_system():
    """Display billing system interface"""
    st.header("💰 Billing System")
    
    inventory = st.session_state.inventory
    billing = st.session_state.billing
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🛒 Shopping Cart")
        
        # Add products to cart
        if inventory.products:
            product_id = st.selectbox("Select Product", list(inventory.products.keys()))
            
            if product_id:
                product = inventory.get_product(product_id)
                st.write(f"**Product:** {product.name}")
                st.write(f"**Price:** Rs{product.price:.2f}")
                st.write(f"**Available Stock:** {product.quantity}")
                
                quantity = st.number_input("Quantity", min_value=1, max_value=product.quantity, step=1)
                
                if st.button("Add to Cart"):
                    # Check if product already in cart
                    item_exists = False
                    for item in st.session_state.cart:
                        if item['product_id'] == product_id:
                            item['quantity'] += quantity
                            item['total'] = item['price'] * item['quantity']
                            item_exists = True
                            break
                    
                    if not item_exists:
                        st.session_state.cart.append({
                            'product_id': product_id,
                            'name': product.name,
                            'price': product.price,
                            'quantity': quantity,
                            'total': product.price * quantity
                        })
                    
                    st.success(f"Added {quantity} x {product.name} to cart!")
                    st.rerun()
        else:
            st.info("No products available.")
        
        # Display cart
        if st.session_state.cart:
            st.subheader("Cart Contents")
            total_amount = 0
            
            for i, item in enumerate(st.session_state.cart):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**{item['name']}**")
                
                with col2:
                    st.write(f"Rs{item['price']:.2f}")
                
                with col3:
                    st.write(f"x{item['quantity']}")
                
                with col4:
                    st.write(f"Rs{item['total']:.2f}")
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
                
                total_amount += item['total']
            
            st.write("---")
            st.write(f"**Total Amount: Rs{total_amount:.2f}**")
            
            if st.button("Clear Cart"):
                st.session_state.cart.clear()
                st.rerun()
        else:
            st.info("Cart is empty.")
    
    with col2:
        st.subheader("💳 Payment")
        
        if st.session_state.cart:
            total_amount = sum(item['total'] for item in st.session_state.cart)
            st.write(f"**Total:** Rs{total_amount:.2f}")
            
            customer_name = st.text_input("Customer Name", value="Walk-in Customer")
            payment_amount = st.number_input("Payment Amount (Rs)", min_value=0.0, step=0.01)
            
            if st.button("Process Payment", type="primary"):
                if payment_amount >= total_amount:
                    success, result = billing.process_payment(st.session_state.cart, payment_amount, customer_name)
                    
                    if success:
                        st.success("Payment processed successfully!")
                        st.write(f"**Transaction ID:** {result['transaction_id']}")
                        st.write(f"**Change:** Rs{result['change']:.2f}")
                        
                        # Clear cart
                        st.session_state.cart.clear()
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.error(f"Insufficient payment. Total: Rs{total_amount:.2f}")
        else:
            st.info("Add items to cart first.")

def show_low_stock_alerts():
    """Display low stock alerts"""
    st.header("⚠️ Low Stock Alerts")
    
    inventory = st.session_state.inventory
    low_stock_products = inventory.get_low_stock_products()
    
    if low_stock_products:
        st.warning(f"**{len(low_stock_products)} products have low stock!**")
        
        # Display low stock products
        for product in low_stock_products:
            with st.expander(f"⚠️ {product.name} (ID: {product.product_id})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Current Stock", product.quantity)
                
                with col2:
                    st.metric("Threshold", product.min_stock_threshold)
                
                with col3:
                    st.metric("Category", product.category)
                
                # Quick stock update
                st.subheader("Quick Stock Update")
                col1, col2 = st.columns(2)
                
                with col1:
                    add_stock = st.number_input("Add Stock", min_value=1, step=1, key=f"add_{product.product_id}")
                    if st.button(f"Add {add_stock} to Stock", key=f"btn_add_{product.product_id}"):
                        success, message = inventory.update_stock(product.product_id, add_stock)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                
                with col2:
                    st.write(f"**Price:** Rs{product.price:.2f}")
                    st.write(f"**Total Value:** Rs{product.price * product.quantity:.2f}")
        
        # Chart showing low stock products
        st.subheader("📊 Low Stock Overview")
        
        low_stock_data = []
        for product in low_stock_products:
            low_stock_data.append({
                'Product': product.name,
                'Current Stock': product.quantity,
                'Threshold': product.min_stock_threshold,
                'Category': product.category
            })
        
        df = pd.DataFrame(low_stock_data)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Current Stock',
            x=df['Product'],
            y=df['Current Stock'],
            marker_color='red'
        ))
        fig.add_trace(go.Bar(
            name='Threshold',
            x=df['Product'],
            y=df['Threshold'],
            marker_color='orange'
        ))
        
        fig.update_layout(
            title="Low Stock Products",
            xaxis_title="Products",
            yaxis_title="Quantity",
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.success("🎉 All products are well stocked! No low stock alerts.")
        
        # Show stock levels chart
        st.subheader("📊 Current Stock Levels")
        
        if inventory.products:
            stock_data = []
            for product in inventory.products.values():
                stock_data.append({
                    'Product': product.name,
                    'Stock': product.quantity,
                    'Category': product.category
                })
            
            df = pd.DataFrame(stock_data)
            
            fig = px.bar(
                df,
                x='Product',
                y='Stock',
                color='Category',
                title="Current Stock Levels by Product"
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

def show_sales_reports():
    """Display sales reports and analytics"""
    st.header("📈 Sales Reports & Analytics")
    
    billing = st.session_state.billing
    
    if billing.sales_history:
        # Convert to DataFrame
        sales_data = []
        for transaction in billing.sales_history:
            sales_data.append({
                'Transaction ID': transaction['transaction_id'],
                'Customer': transaction['customer_name'],
                'Date': datetime.datetime.fromisoformat(transaction['timestamp']).strftime('%Y-%m-%d'),
                'Time': datetime.datetime.fromisoformat(transaction['timestamp']).strftime('%H:%M:%S'),
                'Total Amount': transaction['total_amount'],
                'Payment Amount': transaction['payment_amount'],
                'Change': transaction['change'],
                'Items Count': len(transaction['items'])
            })
        
        df = pd.DataFrame(sales_data)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Transactions", len(df))
        
        with col2:
            total_sales = df['Total Amount'].sum()
            st.metric("Total Sales", f"Rs{total_sales:,.2f}")
        
        with col3:
            avg_transaction = df['Total Amount'].mean()
            st.metric("Average Transaction", f"Rs{avg_transaction:.2f}")
        
        with col4:
            total_items = df['Items Count'].sum()
            st.metric("Total Items Sold", total_items)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Sales Over Time")
            
            # Group by date
            daily_sales = df.groupby('Date')['Total Amount'].sum().reset_index()
            daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])
            
            fig = px.line(
                daily_sales,
                x='Date',
                y='Total Amount',
                title="Daily Sales Trend"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Transaction Distribution")
            
            fig = px.histogram(
                df,
                x='Total Amount',
                nbins=10,
                title="Transaction Amount Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Transaction details
        st.subheader("📋 Transaction Details")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            date_filter = st.date_input("Filter by Date", value=None)
        
        with col2:
            customer_filter = st.selectbox("Filter by Customer", ["All"] + list(df['Customer'].unique()))
        
        # Apply filters
        filtered_df = df.copy()
        
        if date_filter:
            filtered_df = filtered_df[filtered_df['Date'] == date_filter.strftime('%Y-%m-%d')]
        
        if customer_filter != "All":
            filtered_df = filtered_df[filtered_df['Customer'] == customer_filter]
        
        # Display filtered data
        st.dataframe(
            filtered_df[['Transaction ID', 'Customer', 'Date', 'Time', 'Total Amount', 'Items Count']],
            use_container_width=True
        )
        
        # Export option
        if st.button("📥 Export Sales Data"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"sales_report_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    else:
        st.info("No sales data available yet. Start making sales to see reports here!")

def show_error_monitor():
    """Display comprehensive error monitoring and system diagnostics"""
    st.header("🔍 Error Monitor & System Diagnostics")
    
    inventory = st.session_state.inventory
    billing = st.session_state.billing
    
    # System Status Overview
    st.subheader("📊 System Status Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # File system status
        inventory_file_exists = os.path.exists("inventory.json")
        sales_file_exists = os.path.exists("sales.json")
        
        if inventory_file_exists and sales_file_exists:
            st.success("✅ Files: All Present")
        elif inventory_file_exists or sales_file_exists:
            st.warning("⚠️ Files: Partial")
        else:
            st.error("❌ Files: Missing")
    
    with col2:
        # Data integrity
        try:
            product_count = len(inventory.products)
            sales_count = len(billing.sales_history)
            st.success(f"✅ Data: {product_count} products, {sales_count} sales")
        except Exception as e:
            st.error(f"❌ Data Error: {str(e)}")
    
    with col3:
        # Low stock check
        try:
            low_stock_count = len(inventory.get_low_stock_products())
            if low_stock_count == 0:
                st.success("✅ Stock: All Good")
            else:
                st.error(f"🚨 Stock: {low_stock_count} low")
        except Exception as e:
            st.error(f"❌ Stock Error: {str(e)}")
    
    with col4:
        # System health
        try:
            # Test basic operations
            inventory.save_inventory()
            billing.save_sales_history()
            st.success("✅ System: Healthy")
        except Exception as e:
            st.error(f"❌ System Error: {str(e)}")
    
    st.markdown("---")
    
    # Detailed Error Analysis
    st.subheader("🔍 Detailed Error Analysis")
    
    # File System Errors
    st.subheader("📁 File System Errors")
    
    file_errors = []
    
    # Check inventory file
    if os.path.exists("inventory.json"):
        try:
            with open("inventory.json", "r") as f:
                data = json.load(f)
            st.success("✅ inventory.json: Readable and valid JSON")
        except json.JSONDecodeError as e:
            file_errors.append(f"❌ inventory.json: Invalid JSON - {str(e)}")
        except PermissionError:
            file_errors.append("❌ inventory.json: Permission denied")
        except Exception as e:
            file_errors.append(f"❌ inventory.json: Error - {str(e)}")
    else:
        file_errors.append("❌ inventory.json: File not found")
    
    # Check sales file
    if os.path.exists("sales.json"):
        try:
            with open("sales.json", "r") as f:
                data = json.load(f)
            st.success("✅ sales.json: Readable and valid JSON")
        except json.JSONDecodeError as e:
            file_errors.append(f"❌ sales.json: Invalid JSON - {str(e)}")
        except PermissionError:
            file_errors.append("❌ sales.json: Permission denied")
        except Exception as e:
            file_errors.append(f"❌ sales.json: Error - {str(e)}")
    else:
        file_errors.append("❌ sales.json: File not found")
    
    if file_errors:
        for error in file_errors:
            st.error(error)
    else:
        st.success("✅ All files are accessible and valid")
    
    # Data Validation Errors
    st.subheader("📊 Data Validation Errors")
    
    data_errors = []
    
    # Check product data integrity
    for product_id, product in inventory.products.items():
        if product.price < 0:
            data_errors.append(f"❌ Product {product_id}: Negative price (Rs{product.price})")
        if product.quantity < 0:
            data_errors.append(f"❌ Product {product_id}: Negative quantity ({product.quantity})")
        if not product.name or not product.name.strip():
            data_errors.append(f"❌ Product {product_id}: Empty or invalid name")
        if not product_id or not product_id.strip():
            data_errors.append(f"❌ Product: Empty ID for product '{product.name}'")
        if product.category not in ["Electronics", "Stationery", "Kitchen", "Clothing", "General"]:
            data_errors.append(f"⚠️ Product {product_id}: Unusual category '{product.category}'")
    
    # Check sales data integrity
    for transaction in billing.sales_history:
        if transaction['total_amount'] < 0:
            data_errors.append(f"❌ Transaction {transaction['transaction_id']}: Negative total amount")
        if transaction['payment_amount'] < transaction['total_amount']:
            data_errors.append(f"❌ Transaction {transaction['transaction_id']}: Insufficient payment")
        if not transaction.get('customer_name'):
            data_errors.append(f"❌ Transaction {transaction['transaction_id']}: Missing customer name")
        if not transaction.get('items') or len(transaction['items']) == 0:
            data_errors.append(f"❌ Transaction {transaction['transaction_id']}: No items")
    
    if data_errors:
        st.error(f"**Found {len(data_errors)} data validation errors:**")
        for error in data_errors[:20]:  # Show first 20 errors
            st.error(error)
        if len(data_errors) > 20:
            st.warning(f"... and {len(data_errors) - 20} more errors")
    else:
        st.success("✅ No data validation errors found")
    
    # System Performance
    st.subheader("⚡ System Performance")
    
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        st.write("**Memory Usage:**")
        try:
            import psutil
            memory = psutil.virtual_memory()
            st.write(f"- Available: {memory.available / (1024**3):.1f} GB")
            st.write(f"- Used: {memory.percent}%")
        except ImportError:
            st.info("Install psutil for memory monitoring")
    
    with perf_col2:
        st.write("**File Sizes:**")
        try:
            if os.path.exists("inventory.json"):
                size = os.path.getsize("inventory.json")
                st.write(f"- inventory.json: {size} bytes")
            if os.path.exists("sales.json"):
                size = os.path.getsize("sales.json")
                st.write(f"- sales.json: {size} bytes")
        except Exception as e:
            st.error(f"Error checking file sizes: {e}")
    
    # Error Recovery Actions
    st.subheader("🔧 Error Recovery Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Data"):
            try:
                inventory.load_inventory()
                billing.load_sales_history()
                st.success("Data refreshed successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error refreshing data: {e}")
    
    with col2:
        if st.button("💾 Backup Data"):
            try:
                import shutil
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                if os.path.exists("inventory.json"):
                    shutil.copy("inventory.json", f"inventory_backup_{timestamp}.json")
                if os.path.exists("sales.json"):
                    shutil.copy("sales.json", f"sales_backup_{timestamp}.json")
                st.success("Data backed up successfully!")
            except Exception as e:
                st.error(f"Error creating backup: {e}")
    
    with col3:
        if st.button("🧹 Clear Error Log"):
            st.success("Error log cleared!")
            st.rerun()
    
    # System Logs
    st.subheader("📋 System Logs")
    
    # Create a simple log display
    log_entries = []
    
    # Add system startup log
    log_entries.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] System initialized")
    
    # Add product count log
    log_entries.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Loaded {len(inventory.products)} products")
    
    # Add sales count log
    log_entries.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Loaded {len(billing.sales_history)} transactions")
    
    # Add low stock log
    low_stock_count = len(inventory.get_low_stock_products())
    if low_stock_count > 0:
        log_entries.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] WARNING: {low_stock_count} low stock items")
    
    # Display logs
    for entry in log_entries:
        if "WARNING" in entry or "ERROR" in entry:
            st.error(entry)
        else:
            st.info(entry)

if __name__ == "__main__":
    main()
