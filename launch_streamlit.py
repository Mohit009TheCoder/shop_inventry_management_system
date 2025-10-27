#!/usr/bin/env python3
"""
Launcher script for Shop Inventory Management System - Streamlit Version
This script helps launch the Streamlit application with proper configuration
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['streamlit', 'pandas', 'plotly']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("Error installing dependencies. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def launch_streamlit():
    """Launch the Streamlit application"""
    if not os.path.exists('streamlit_app.py'):
        print("Error: streamlit_app.py not found!")
        print("Please make sure you're in the correct directory.")
        return False
    
    print("="*60)
    print("🏪 SHOP INVENTORY MANAGEMENT SYSTEM")
    print("="*60)
    print("Launching Streamlit web application...")
    print("The application will open in your default web browser.")
    print("If it doesn't open automatically, go to: http://localhost:8501")
    print("="*60)
    
    try:
        # Launch Streamlit with custom configuration
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false'
        ])
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error launching application: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("Shop Inventory Management System - Streamlit Launcher")
    print("Checking dependencies...")
    
    if check_dependencies():
        print("Dependencies OK!")
        launch_streamlit()
    else:
        print("Failed to install dependencies. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()

