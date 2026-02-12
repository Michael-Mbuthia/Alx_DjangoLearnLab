# Advanced API Project

This folder contains a small Django + Django REST Framework (DRF) project that exposes CRUD endpoints for a `Book` model.

## Setup

From the repo root (where `.venv/` lives), run:

- `cd advanced-api-project`
- `C:/Users/jm744/Documents/Alx_DjangoLearnLab/.venv/Scripts/python.exe manage.py migrate`
- (optional) `C:/Users/jm744/Documents/Alx_DjangoLearnLab/.venv/Scripts/python.exe manage.py createsuperuser`
- `C:/Users/jm744/Documents/Alx_DjangoLearnLab/.venv/Scripts/python.exe manage.py runserver`

## Endpoints

All endpoints are defined in `api/urls.py` and implemented using DRF generic views in `api/views.py`.

### Read (public)

- `GET /books/` — list all books
  - Filtering (DjangoFilterBackend):
    - `?author=<author_id>`
    - `?author__name__icontains=<substring>`
    - `?title__icontains=<substring>`
    - `?publication_year=<year>`
    - `?publication_year__gte=<year>`
    - `?publication_year__lte=<year>`
  - Search (SearchFilter):
    - `?search=<text>` (searches title and author name)
  - Ordering (OrderingFilter):
    - `?ordering=title` or `?ordering=-publication_year`
- `GET /books/<pk>/` — retrieve a single book by id

### Write (authenticated)

- `POST /books/create/` — create a book
- `PUT/PATCH /books/<pk>/update/` — update a book
- `DELETE /books/<pk>/delete/` — delete a book

Permissions are applied per-view using DRF permission classes:

- List/Detail: `AllowAny`
- Create/Update/Delete: `IsAuthenticated`

## Authentication

This project includes DRF’s browsable API login routes:

- `GET /api-auth/login/`
- `GET /api-auth/logout/`

You can also use Basic Auth from tools like curl/Postman.

## Testing

This project uses Django’s built-in test framework (based on Python’s `unittest`).

Test database behavior:
- When you run tests, Django automatically creates a separate test database (e.g. `test_db.sqlite3` for SQLite), runs migrations, executes tests, then destroys it.
- This keeps your development database (`db.sqlite3`) safe from test data.

Run the API tests:
- `C:/Users/jm744/Documents/Alx_DjangoLearnLab/.venv/Scripts/python.exe manage.py test api`

What the tests cover:
- Public read access for list/detail endpoints
- Auth-required write access for create/update/delete endpoints
- Model/serializer validation (future `publication_year` is rejected)
- Filtering/search/ordering behaviors on the list endpoint

## Manual testing examples

### List books (no auth)

- `curl http://127.0.0.1:8000/books/`

### Filter / search / ordering examples

- Filter by author id:
  - `curl "http://127.0.0.1:8000/books/?author=1"`
- Filter by title substring:
  - `curl "http://127.0.0.1:8000/books/?title__icontains=potter"`
- Search (title + author name):
  - `curl "http://127.0.0.1:8000/books/?search=potter"`
- Order by newest publication year first:
  - `curl "http://127.0.0.1:8000/books/?ordering=-publication_year"`

### Create a book (auth required)

- `curl -u <username>:<password> -H "Content-Type: application/json" -d "{\"title\": \"My Book\", \"publication_year\": 2020, \"author\": 1}" http://127.0.0.1:8000/books/create/`

### Permission check

- Try the same POST without `-u <username>:<password>` — it should fail (401/403).

## Notes on customization

- Filtering is implemented in `BookListView.get_queryset()` using query params.
- Validation for `publication_year` is implemented in `api/serializers.py` and rejects future years.
