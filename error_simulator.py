#!/usr/bin/env python3
"""
Error Simulation Script for Shop Inventory Management System
This script creates various types of errors to test the error monitoring system
"""

import json
import os
import shutil
from datetime import datetime

def create_error_scenarios():
    """Create various error scenarios to test error monitoring"""
    
    print("="*60)
    print("ERROR SIMULATION FOR SHOP INVENTORY MANAGEMENT SYSTEM")
    print("="*60)
    
    # Create backup of original files
    if os.path.exists("inventory.json"):
        shutil.copy("inventory.json", "inventory_backup.json")
        print("✅ Created backup of inventory.json")
    
    if os.path.exists("sales.json"):
        shutil.copy("sales.json", "sales_backup.json")
        print("✅ Created backup of sales.json")
    
    print("\nCreating error scenarios...")
    
    # Scenario 1: Corrupt inventory file
    print("\n1. Creating corrupted inventory file...")
    with open("inventory.json", "w") as f:
        f.write('{"invalid": json, "corrupted": true')  # Invalid JSON
    print("❌ inventory.json corrupted with invalid JSON")
    
    # Scenario 2: Missing sales file
    print("\n2. Removing sales file...")
    if os.path.exists("sales.json"):
        os.remove("sales.json")
    print("❌ sales.json removed")
    
    # Scenario 3: Create inventory with invalid data
    print("\n3. Creating inventory with invalid data...")
    invalid_inventory = [
        {
            "product_id": "",  # Empty ID
            "name": "",  # Empty name
            "price": -100.0,  # Negative price
            "quantity": -5,  # Negative quantity
            "category": "InvalidCategory",  # Invalid category
            "min_stock_threshold": 10
        },
        {
            "product_id": "P001",
            "name": "Valid Product",
            "price": 100.0,
            "quantity": 5,
            "category": "Electronics",
            "min_stock_threshold": 10
        }
    ]
    
    with open("inventory.json", "w") as f:
        json.dump(invalid_inventory, f, indent=2)
    print("❌ inventory.json created with invalid data")
    
    # Scenario 4: Create sales with invalid data
    print("\n4. Creating sales with invalid data...")
    invalid_sales = [
        {
            "transaction_id": "TXN_INVALID",
            "customer_name": "",  # Empty customer name
            "timestamp": "invalid-timestamp",  # Invalid timestamp
            "items": [],  # Empty items
            "total_amount": -50.0,  # Negative total
            "payment_amount": 30.0,  # Insufficient payment
            "change": 80.0
        }
    ]
    
    with open("sales.json", "w") as f:
        json.dump(invalid_sales, f, indent=2)
    print("❌ sales.json created with invalid data")
    
    print("\n" + "="*60)
    print("ERROR SCENARIOS CREATED SUCCESSFULLY!")
    print("="*60)
    print("Now run the Streamlit app to see error monitoring in action:")
    print("streamlit run streamlit_app.py")
    print("\nGo to the 'Error Monitor' page to see all detected errors.")
    print("="*60)

def restore_backup():
    """Restore original files from backup"""
    print("\nRestoring original files...")
    
    if os.path.exists("inventory_backup.json"):
        shutil.copy("inventory_backup.json", "inventory.json")
        os.remove("inventory_backup.json")
        print("✅ Restored inventory.json")
    
    if os.path.exists("sales_backup.json"):
        shutil.copy("sales_backup.json", "sales.json")
        os.remove("sales_backup.json")
        print("✅ Restored sales.json")
    
    print("✅ All files restored successfully!")

def main():
    """Main function"""
    print("Error Simulation Script")
    print("This script creates various error scenarios to test error monitoring.")
    
    choice = input("\nChoose an option:\n1. Create error scenarios\n2. Restore from backup\n3. Exit\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        create_error_scenarios()
    elif choice == "2":
        restore_backup()
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()

