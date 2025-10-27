# 🏪 Shop Inventory Management System - Streamlit Web App

A modern, interactive web-based inventory management system built with Streamlit, featuring real-time dashboards, billing functionality, and automatic low stock alerts.

## ✨ Features

### 📊 **Interactive Dashboard**
- Real-time metrics and KPIs
- Visual charts and graphs using Plotly
- Inventory value tracking
- Sales analytics
- Recent transaction overview

### 📦 **Inventory Management**
- **Add Products**: Easy form-based product addition
- **Update Products**: Modify product details
- **Stock Management**: Add/remove stock with visual feedback
- **Search & Filter**: Find products quickly
- **Remove Products**: Delete products from inventory

### 💰 **Billing System**
- **Shopping Cart**: Add multiple products to cart
- **Payment Processing**: Handle payments with change calculation
- **Receipt Generation**: Automatic transaction records
- **Real-time Stock Updates**: Inventory automatically updates after sales

### ⚠️ **Low Stock Alerts**
- **Visual Alerts**: Clear warnings for low stock items
- **Interactive Dashboard**: Dedicated low stock management page
- **Quick Stock Updates**: One-click stock replenishment
- **Threshold Management**: Configurable alert thresholds (default: < 10 items)

### 📈 **Sales Reports & Analytics**
- **Transaction History**: Complete sales records
- **Visual Charts**: Sales trends and distributions
- **Date Filtering**: Filter reports by date range
- **Customer Analytics**: Track customer transactions
- **Export Functionality**: Download reports as CSV

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run streamlit_app.py
```

### 3. Access the Web Interface
The application will automatically open in your browser at `http://localhost:8501`

## 📱 Web Interface Overview

### **Navigation**
- **Dashboard**: Overview with metrics and charts
- **Inventory Management**: Product CRUD operations
- **Billing System**: Shopping cart and payment processing
- **Low Stock Alerts**: Dedicated alerts management
- **Sales Reports**: Analytics and transaction history

### **Key Pages**

#### 🏠 Dashboard
- Total products count
- Inventory value
- Low stock items count
- Total sales
- Interactive charts for inventory distribution
- Stock levels visualization
- Recent transactions overview

#### 📦 Inventory Management
- **View Products**: Searchable table with all products
- **Add Product**: Form to add new products
- **Update Product**: Modify existing product details
- **Update Stock**: Add or remove inventory
- **Remove Product**: Delete products

#### 💰 Billing System
- **Shopping Cart**: Add products with quantity selection
- **Payment Processing**: Handle payments and calculate change
- **Real-time Updates**: Stock automatically updates after sales
- **Transaction Records**: Automatic receipt generation

#### ⚠️ Low Stock Alerts
- **Alert Dashboard**: Visual overview of low stock items
- **Quick Actions**: One-click stock updates
- **Interactive Charts**: Low stock visualization
- **Threshold Management**: Configure alert levels

#### 📈 Sales Reports
- **Analytics Dashboard**: Sales metrics and trends
- **Transaction History**: Complete sales records
- **Date Filtering**: Filter by date range
- **Export Options**: Download reports as CSV
- **Visual Charts**: Sales trends and distributions

## 🎨 Modern UI Features

### **Responsive Design**
- Mobile-friendly interface
- Adaptive layouts
- Touch-friendly controls

### **Interactive Elements**
- Real-time data updates
- Interactive charts and graphs
- Form validation
- Success/error notifications

### **Visual Indicators**
- Color-coded stock levels
- Alert badges and warnings
- Progress indicators
- Status badges

## 📊 Data Visualization

### **Charts & Graphs**
- **Pie Charts**: Inventory distribution by category
- **Bar Charts**: Stock levels and sales trends
- **Line Charts**: Sales over time
- **Histograms**: Transaction distributions

### **Interactive Features**
- Hover tooltips
- Zoom and pan capabilities
- Click interactions
- Real-time updates

## 🔧 Technical Features

### **Data Persistence**
- JSON file storage
- Automatic data saving
- Session state management
- Data integrity checks

### **Error Handling**
- Form validation
- Input sanitization
- Graceful error messages
- Data validation

### **Performance**
- Efficient data loading
- Optimized queries
- Caching mechanisms
- Responsive updates

## 📁 File Structure

```
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── inventory.json            # Product data (auto-generated)
├── sales.json               # Sales history (auto-generated)
└── README.md                # This documentation
```

## 🛠️ Customization

### **Styling**
- Custom CSS for enhanced appearance
- Color schemes and themes
- Responsive design elements
- Brand customization

### **Configuration**
- Adjustable stock thresholds
- Custom categories
- Configurable alerts
- Flexible reporting

### **Extensions**
- Additional chart types
- Custom metrics
- Advanced filtering
- Integration capabilities

## 📈 Demo Data

The application includes demo data with:
- **10 Sample Products** across different categories
- **Pre-configured Low Stock Items** to demonstrate alerts
- **Sample Categories**: Electronics, Stationery, Kitchen, Clothing
- **Realistic Pricing** and stock levels

## 🔒 Security Features

- Input validation
- Data sanitization
- Error handling
- Session management

## 🌐 Browser Compatibility

- **Chrome**: Full support
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support

## 📱 Mobile Support

- Responsive design
- Touch-friendly interface
- Mobile-optimized layouts
- Cross-device compatibility

## 🚀 Deployment Options

### **Local Development**
```bash
streamlit run streamlit_app.py
```

### **Cloud Deployment**
- Streamlit Cloud
- Heroku
- AWS
- Google Cloud Platform

### **Docker Support**
```dockerfile
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## 🔄 Updates & Maintenance

- **Automatic Data Backup**: JSON files preserve all data
- **Version Control**: Track changes with Git
- **Regular Updates**: Keep dependencies current
- **Performance Monitoring**: Track application metrics

## 📞 Support

For issues or questions:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure proper file permissions
4. Review the documentation

## 🎯 Future Enhancements

- **User Authentication**: Multi-user access control
- **Advanced Analytics**: More detailed reporting
- **Barcode Integration**: Scan products for quick entry
- **Email Alerts**: Automated low stock notifications
- **API Integration**: Connect with external systems
- **Mobile App**: Native mobile application
- **Cloud Sync**: Multi-device synchronization

---

**Built with ❤️ using Streamlit, Pandas, and Plotly**

The system provides a complete, modern solution for shop inventory management with an intuitive web interface, real-time alerts, and comprehensive analytics.

