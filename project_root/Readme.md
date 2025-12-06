
📚 Expense Tracker & Book Management App

A Django-based web application for managing book categories, tracking distribution expenses, and handling user authentication.  
The project is containerized with Docker and uses PostgreSQL, Redis, Celery, and Nginx for a full production-ready stack.


## 🚀 Features

- **Homepage**: Renders `books/home.html` via `HomeView`.
- **Authentication**:
  - User registration (`RegisterView`)
  - Login / Logout (Django’s built-in auth views)
- **Book Categories**:
  - List, create, update, delete categories
- **Books**:
  - List, create, update, delete books
  - Track distribution expenses
- **Import & Reports**:
  - Upload CSV/XLSX files for bulk import
  - Generate expense reports by category/publisher
- **Caching**:
  - Redis-backed caching for aggregate queries
- **Rate Limiting**:
  - Protects import endpoints with `django_ratelimit`

---

## 🛠️ Tech Stack

- **Backend**: Django 5.x
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **Task Queue**: Celery (worker + beat)
- **Web Server**: Gunicorn
- **Reverse Proxy**: Nginx
- **Containerization**: Docker & Docker Compose
- **Frontend**: Django templates (`base.html`, `books/home.html`, etc.)

---

## 📂 Project Structure

```
project_root/
├── books/                     # App for books & categories
│   ├── templates/books/       # App-specific templates
│   │   ├── base.html
│   │   └── home.html
│   ├── views.py               # Class-based views
│   ├── urls.py                # App routes
│   └── models.py              # Book & Category models
├── expense_tracker/            # Project config
│   ├── urls.py                # Root URLconf
│   └── settings.py            # Django settings
├── templates/                  # Global templates
├── manage.py
├── docker-compose.yml
└── requirements.txt
```

---

## ⚙️ Setup & Installation

1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. **Start services with Docker Compose**:
   ```bash
   docker-compose up --build -d
   ```

3. **Run migrations**:
   ```bash
   docker exec -it project_root-web-1 python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   docker exec -it project_root-web-1 python manage.py createsuperuser
   ```

5. **Access the app**:
   - Homepage → `http://localhost/`
   - Admin → `http://localhost/admin/`

---

## 🔑 Default Routes

- `/` → Homepage (`HomeView`)
- `/books/` → Books app routes
- `/books/categories/` → Category list
- `/books/books/` → Book list
- `/books/import/` → Import view
- `/books/report/` → Report view
- `/login/` → Login
- `/logout/` → Logout
- `/register/` → User registration

---

## 📝 Notes

- Ensure `base.html` exists in `templates/` or `books/templates/books/` and is referenced correctly.
- Static files are served via Nginx (`/static/`).
- Media uploads are stored in `/media/`.

---

## 📌 Roadmap

- Add REST API endpoints with Django REST Framework
- Enhance reporting with charts/graphs
- Implement user roles & permissions
- Add unit tests and CI/CD pipeline

---

## 👨‍💻 Author

Developed by **Rowland**  
Location: Lagos, Nigeria  
Date: December 2025
```

---

👉 This README.md gives a clear overview of your app, its features, stack, setup instructions, and routes.  

Would you like me to also add **screenshots placeholders** (e.g., `![Homepage Screenshot](docs/home.png)`) so you can later drop in images of your homepage and admin panel?