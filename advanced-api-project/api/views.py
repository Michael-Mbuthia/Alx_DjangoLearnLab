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

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Book

from .serializers import BookSerializer


class BookListView(generics.ListAPIView):

    """List all books.

    Filtering / Search / Ordering:
        This view integrates DRF’s filtering capabilities using:
        - DjangoFilterBackend: structured filtering via query params
        - SearchFilter: text search via `?search=`
        - OrderingFilter: ordering via `?ordering=`

    Examples:
        - Filter by author id:           /books/?author=1
        - Filter by author name:         /books/?author__name__icontains=rowling
        - Filter by title substring:     /books/?title__icontains=potter
        - Filter by year (exact):        /books/?publication_year=2020
        - Filter by year range:          /books/?publication_year__gte=2000&publication_year__lte=2020
        - Search:                        /books/?search=potter
        - Order by year desc:            /books/?ordering=-publication_year
    """

    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # DRF filter backends (also configured globally in REST_FRAMEWORK)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # DjangoFilterBackend
    filterset_fields = {
        "title": ["exact", "icontains"],
        "publication_year": ["exact", "gte", "lte"],
        "author": ["exact"],
        "author__name": ["exact", "icontains"],
    }

    # SearchFilter
    search_fields = ["title", "author__name"]

    # OrderingFilter
    ordering_fields = ["id", "title", "publication_year", "author"]
    ordering = ["title"]


class BookDetailView(generics.RetrieveAPIView):

    """Retrieve a single book by id (pk).

    Public (no auth required).
    """

    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):

    """Create a new book.

    Authenticated users only.

    DRF handles JSON parsing + serializer validation (including the custom
    `publication_year` validation in BookSerializer).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):

    """Update an existing book.

    Authenticated users only.

    Supports PUT and PATCH.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["put", "patch", "options", "head"]


class BookDeleteView(generics.DestroyAPIView):

    """Delete a book.

    Authenticated users only.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
