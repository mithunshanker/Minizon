# 🛒 Minizon — Django E-commerce Web App

A modern and fully-functional e-commerce website built with Django and PostgreSQL, deployed live on Render.

🌐 **Live Demo**: [https://minizon.onrender.com](https://minizon.onrender.com)

---

## 🚀 Features

- User Authentication (Sign up, Login, Logout)
- Product Listings with Category Filtering
- Product Details Page
- Add to Cart / Remove from Cart / Update Quantity
- Checkout Flow with Address Form
- Order Placement and Management
- Order Cancellation within 24 hours
- Admin Dashboard with:
  - Order status change (e.g., mark as fulfilled)
  - Inventory management
  - Business metrics & charts
- Media support for product images via Unsplash
- Responsive UI with TailwindCSS

## 🛠️ Tech Stack

- **Backend**: Django, PostgreSQL
- **Frontend**: HTML, TailwindCSS
- **Admin Styling**: django-admin-interface, import_export
- **Media & Demo Data**: Unsplash API, Faker
- **Hosting**: Render

---

## 📁 Folder Structure (Important Directories)

ecommerce/
├── manage.py
├── ecommerce/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── store/
│ ├── models.py
│ ├── views/
│ │ ├── cart_views.py
│ │ ├── auth_views.py
│ │ └── order_views.py
│ ├── templates/
│ │ ├── cart.html
│ │ ├── product_detail.html
│ │ └── ...
│ ├── static/
│ ├── admin.py
│ ├── urls.py
│ └── management/
│ └── commands/
│ └── seed_data.py


---

## 👤 Admin Dashboard Features

- Filter orders by status, user, or date
- Inline editing of order items
- One-click cancel or fulfill orders



Admin panel URL: `https://minizon.onrender.com/admin/`

---

## 🚀 How to Run Locally

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/minizon.git
   cd minizon
2. **Create and activate the virtual environment**
   ```bash
   python3 -m venv env
   source env/bin/activate  # Windows: env\Scripts\activate
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
4. **Set up .env file**
   ```bash
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your host
    DB_PORT=your port
5. **Apply migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
6. **Create a superuser**
   ```bash
    python manage.py createsuperuser
7. **Run the server**
   ```bash
   python manage.py runserver



