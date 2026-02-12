"""api.urls

URL routes for the Book API.

Each view has a distinct endpoint as requested:
    - /books/                 -> list all books
    - /books/<pk>/            -> retrieve a single book
    - /books/create/          -> create a new book (auth required)
    - /books/<pk>/update/     -> update an existing book (auth required)
    - /books/<pk>/delete/     -> delete a book (auth required)

Permissions:
    Read endpoints are public; write endpoints require authentication.
"""

from django.urls import path

from .views import (
    BookCreateView,
    BookDeleteView,
    BookDetailView,
    BookListView,
    BookUpdateView,
)

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
]
