# 🍗 Jahangeer Chicken Center - Official Website & Management System

A production-quality website and business management application built for **Jahangeer Chicken Center** (Secunderabad, Telangana).

---

## 📌 Business Overview

* **Shop Name:** Jahangeer Chicken Center
* **Supplier Brand:** SNEHA Fresh Chicken *(Chicken supplied by Sneha)*
* **Business Type:** Fresh Chicken Retail, Wholesale, and Company / Bulk Orders
* **Address:** Jahangir Chicken Center, Opposite Army College of Dental Sciences, Rajiv Swagruha ABHIMAAN Project, Secunderabad, Telangana - 500087
* **Google Maps:** [https://maps.app.goo.gl/sj876gsP9mo6CVot5?g_st=ac](https://maps.app.goo.gl/sj876gsP9mo6CVot5?g_st=ac)
* **Phone:** `9908014554` | `6302113176`
* **WhatsApp:** `9908014554`
* **Opening Hours:** Every day from 7:00 AM to 10:00 PM

---

## ✨ Features

### 🛍️ Customer Experience
- **Live Products & Database Prices:** 9 fresh chicken cuts with prices managed dynamically from the database.
- **Custom Cutting Options:** Curry Cut, Small Pieces, Large Pieces, Biryani Cut, 8/12/16 Pieces, Whole Chicken, and Custom Cutting.
- **Easy Pickup Order Builder:** Select items, quantity, cutting preferences, and special instructions.
- **Instant WhatsApp Integration:** Creates pre-filled WhatsApp order messages sent directly to `9908014554`.
- **Direct Calling:** Click-to-call buttons (`tel:9908014554` and `tel:6302113176`) across mobile & desktop headers.
- **Bulk & Company Orders Page:** Specialized section for Restaurants, Hotels, Caterers, Function Halls, and Events.
- **Multilingual Support (i18n):** Real-time language switcher for **English**, **Telugu**, and **Hindi**.
- **Customer Reviews:** Verified customer review submission with admin moderation queue.
- **Mobile-First Responsive Design:** Sticky action bar (Call & WhatsApp) on mobile screens for seamless user conversion.

### 🛡️ Admin Dashboard (`/admin/login`)
- **KPI Metrics:** Today's Revenue, Today's Orders, Pending Orders, Completed Orders, Total Chicken Sold (KG), Bulk Orders, Weekly/Monthly/Total Revenue.
- **Interactive Analytics:** 7-Day Revenue Trend Line Chart & Product Sales Volume Doughnut Chart.
- **Product & Price Management:** Add products, update prices per KG live, toggle availability (In Stock / Out of Stock), upload product images, and deactivate items.
- **Order Management:** View orders, inspect customer cutting instructions, update status (`New` ➔ `Accepted` ➔ `Preparing` ➔ `Ready for Pickup` ➔ `Completed` / `Cancelled`). Automatically records revenue when order is marked `Completed`.
- **Revenue Tracking:** View transactions breakdown and log manual offline counter/walk-in cash & UPI sales.
- **Bulk Enquiry Management:** Manage leads from restaurants, hotels, and commercial buyers.
- **Review Moderation:** Approve, hide, or delete customer reviews before they appear publicly.
- **Website Settings:** Update phone numbers, opening hours, address, Google Maps link, Instagram URL, and change admin password.

---

## 🛠️ Tech Stack

* **Backend:** Python 3 (Flask, Flask-SQLAlchemy, Werkzeug)
* **Database:** SQLite (Production-ready relational schema, easily migratable to PostgreSQL/MySQL)
* **Frontend:** HTML5, CSS3, Tailwind CSS, JavaScript (Vanilla JS, Chart.js for analytics, custom i18n engine)
* **Security:** Password hashing (Werkzeug PBKDF2), session authentication, route protection, input sanitization.

---

## 📂 Project Structure

```
Shop/
├── app.py                     # Main Flask application entry point & API routes
├── config.py                  # Environment & Flask configuration
├── models.py                  # SQLAlchemy Database Models (Admin, Product, Order, etc.)
├── seed.py                    # Database initialization & initial product/setting seeder
├── utils.py                   # Helper functions (Auth decorators, WhatsApp link generator)
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables configuration
├── .env.example               # Template environment configuration
├── test_app.py                # Automated integration test suite
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom styling & scrollbar fixes
│   ├── js/
│   │   ├── i18n.js            # Multilingual translations (EN, TE, HI)
│   │   ├── cart.js            # Customer cart & WhatsApp prefilled order builder
│   │   └── admin.js           # Admin dashboard charts & modal handlers
│   ├── images/
│   │   ├── logo.svg           # Jahangeer Chicken Center logo
│   │   ├── sneha_logo.svg     # Sneha Fresh Chicken supplier badge
│   │   ├── shop_front.svg     # Storefront illustration
│   │   └── products/          # SVG product image graphics
│   └── uploads/               # User-uploaded product images directory
│
└── templates/
    ├── base.html              # Master layout (Header, Nav, Footer, Mobile Sticky Bar)
    ├── index.html             # Home page
    ├── products.html          # Product catalog & prices
    ├── about.html             # About Us page & Sneha supplier info
    ├── bulk_orders.html       # Bulk & Company orders page
    ├── reviews.html           # Customer reviews page
    ├── contact.html           # Contact details & directions page
    ├── admin/
    │   ├── login.html         # Secure admin login page
    │   ├── base_admin.html    # Admin layout & sidebar
    │   ├── dashboard.html     # Dashboard KPIs & charts
    │   ├── products.html      # Product & price management
    │   ├── orders.html        # Order management
    │   ├── revenue.html       # Revenue analytics & manual walk-in logger
    │   ├── bulk.html          # Bulk enquiries list
    │   ├── reviews.html       # Review moderation queue
    │   └── settings.html      # Website & business settings editor
    └── errors/
        ├── 404.html           # Page not found error template
        └── 500.html           # Server error template
```

---

## 🚀 Easy Local Execution Instructions

Follow these step-by-step instructions to run the application on your computer.

### Step 1: Open Terminal in Project Folder
Open PowerShell or Command Prompt in the `C:\Study\Shop` directory.

### Step 2: Activate Virtual Environment
Run:
```powershell
.\venv\Scripts\activate
```

### Step 3: Initialize & Seed the Database
Run:
```powershell
python seed.py
```
*(This creates the database tables, seeds default admin login, website settings, and initial 9 products with current prices).*

### Step 4: Start the Application Server
Run:
```powershell
python app.py
```

### Step 5: Open in Your Browser
Open your browser and navigate to:
* **Public Website:** `http://127.0.0.1:5000/`
* **Admin Dashboard:** `http://127.0.0.1:5000/admin/login`

---

## 🔐 Initial Admin Login Credentials

* **Username:** `admin`
* **Password:** *(Set via ADMIN_PASSWORD environment variable or in .env)*

*(You can change the admin password anytime inside **Admin Dashboard ➔ Website Settings**).*

---

## 📘 Admin User Guide (Simple Instructions)

### 1. How to Change Prices
1. Log into the Admin Dashboard (`http://127.0.0.1:5000/admin/login`).
2. Click **Products & Prices** in the left menu.
3. Click the **Edit Price / Details** button next to any product.
4. Enter the new **Price per KG (₹)** and click **Save Changes**.
5. The updated price immediately reflects across the website!

### 2. How to Add a New Product
1. Go to **Products & Prices**.
2. Click the **+ Add New Product** button at the top right.
3. Fill in the Product Name, Category, Price per KG, and optional Image.
4. Click **Add Product**.

### 3. How to Mark Products In Stock / Out of Stock
1. Go to **Products & Prices**.
2. Click the **In Stock / Out of Stock** button next to any product to toggle its availability.

### 4. How to Manage Pickup Orders
1. Go to **Orders** in the admin menu.
2. View incoming customer orders, requested cutting style, and special instructions.
3. Select a status from the dropdown (`New`, `Accepted`, `Preparing`, `Ready for Pickup`, `Completed`, `Cancelled`).
4. *Note: When an order status is updated to `Completed`, its total amount is automatically added to Today's Revenue!*

### 5. How to Record Walk-in / Counter Sales
1. Go to **Revenue Tracking** in the admin menu.
2. In the "Record Walk-in / Counter Sale Transaction" form, enter the sale amount (e.g. ₹450), select payment method (Cash/UPI), and click **+ Record Sale Transaction**.

### 6. How to Moderate Customer Reviews
1. Go to **Customer Reviews** in the admin menu.
2. Click **Approve & Publish** to show a review on the website, or **Delete** to remove it.

### 7. How to Update Phone Numbers / Business Info
1. Go to **Website Settings** in the admin menu.
2. Update the phone numbers, opening hours, Google Maps link, or Instagram URL.
3. Click **Save All Settings**.

---

## 🌐 Production Deployment Instructions

To put this website online for customers:

### Option A: Render.com (Recommended Free/Easy Hosting)
1. Push this project code to a GitHub repository.
2. Create a free account on [Render.com](https://render.com).
3. Click **New ➔ Web Service** and connect your GitHub repo.
4. Set:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && python seed.py`
   - **Start Command:** `gunicorn app:app` (add `gunicorn` to requirements.txt)
5. Add Environment Variables from `.env`.

### Option B: PythonAnywhere.com
1. Sign up on [PythonAnywhere.com](https://www.pythonanywhere.com).
2. Upload project files or clone git repo.
3. Set Web app WSGI file to point to `app.py`.
4. Run `python seed.py` in Bash console.

---

## 📞 Support & Information
For store queries or updates:
- **Jahangeer Chicken Center**, Secunderabad, Telangana.
- **Phone:** 9908014554 | 6302113176
