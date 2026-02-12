"""api.views

Generic API views for Book CRUD operations.

This module uses Django REST Framework (DRF) generic class-based views to
provide common CRUD behaviors with minimal code:

- ListView:    retrieve all books
- DetailView:  retrieve a single book by primary key
- CreateView:  create a new book (authenticated users only)
- UpdateView:  update an existing book (authenticated users only)
- DeleteView:  delete a book (authenticated users only)

Customization hooks used here:

- `get_queryset()` implements lightweight filtering using query parameters.
- `permission_classes` applies role-based access control:
    * unauthenticated users: read-only access
    * authenticated users: full CRUD
"""

from __future__ import annotations

from rest_framework import generics, permissions

from .models import Book

from .serializers import BookSerializer


class BookListView(generics.ListAPIView):

    """List all books.

    Public (no auth required).

    Optional filters (query params):
        - author: integer author id
        - year: publication_year exact match
        - q: substring match on title
        - ordering: a model field name, e.g. `publication_year` or `-publication_year`
    """

    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Book.objects.select_related("author").all()

        author_id = self.request.query_params.get("author")
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        year = self.request.query_params.get("year")
        if year:
            queryset = queryset.filter(publication_year=year)

        query = self.request.query_params.get("q")
        if query:
            queryset = queryset.filter(title__icontains=query)

        ordering = self.request.query_params.get("ordering")
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset


class BookDetailView(generics.RetrieveAPIView):

    """Retrieve a single book by id (pk).

    Public (no auth required).
    """

    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):

    """Create a new book.

    Authenticated users only.

    DRF handles JSON parsing + serializer validation (including the custom
    `publication_year` validation in BookSerializer).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):

    """Update an existing book.

    Authenticated users only.

    Supports PUT and PATCH.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["put", "patch", "options", "head"]


class BookDeleteView(generics.DestroyAPIView):

    """Delete a book.

    Authenticated users only.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
