# Asset Manager

A Django-based hardware asset management system for tracking hardware assets, assignments, maintenance records, users, and activity logs.

## Features

- Custom Django user model
- Role-Based Access Control
- Django Admin panel
- Django REST Framework API
- JWT authentication
- Asset CRUD
- Location management
- Asset assignment workflow
- Asset return action
- Maintenance logs
- Activity logs
- Dashboard statistics endpoint
- Search, filtering, ordering, and pagination
- GitHub-ready project structure

## Tech Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- django-filter
- SQLite for local development

## Project Structure

```text
asset_manager/
├── apps/
│   ├── accounts/
│   ├── assets/
│   └── common/
├── config/
├── manage.py
├── requirements.txt
└── README.md