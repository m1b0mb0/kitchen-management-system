# Kitchen Management System

A Django web application for managing kitchen operations. The app helps a restaurant team organize cooks, dish types, dishes, and ingredients in one place.

## Features

- User authentication for protected kitchen pages
- Dashboard with kitchen statistics
- CRUD pages for cooks, dish types, dishes, and ingredients
- Dish creation with assigned cooks and ingredient amounts
- Search and pagination on list pages
- Custom `Cook` user model with years of experience
- SQLite database for local development

## Tech Stack

- Python
- Django
- SQLite
- Bootstrap
- django-crispy-forms

## Getting Started

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd kitchen_management_system
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install django django-crispy-forms crispy-bootstrap4
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Open the app in your browser:

   ```text
   http://127.0.0.1:8000/
   ```

## Main Pages

- `/` - dashboard
- `/accounts/login/` - login page
- `/cooks/` - cook list
- `/dish-types/` - dish type list
- `/dishes/` - dish list
- `/ingredients/` - ingredient list
- `/admin/` - Django admin panel

## Project Structure

```text
kitchen_management_system/
|-- kitchen/                     # Main Django app
|   |-- models.py                # Cook, DishType, Dish, Ingredient models
|   |-- views.py                 # Class-based views and dashboard view
|   |-- forms.py                 # Forms and dish ingredient formset
|   `-- urls.py                  # App routes
|-- kitchen_management_system/   # Project settings and root URL config
|-- templates/                   # HTML templates
|-- static/                      # CSS and static assets
`-- manage.py
```
