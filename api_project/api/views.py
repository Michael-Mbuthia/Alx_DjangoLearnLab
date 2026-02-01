"""API views.

Authentication
- DRF Token Authentication is enabled globally in settings.
- Clients must send: Authorization: Token <token>

Permissions
- BookList: any authenticated user may list books.
- BookViewSet: authenticated users may read; only staff users may create/update/delete.
"""

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Book
from .permissions import IsAuthenticatedReadOnlyOrAdminWrite
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """Read-only list endpoint; requires authentication."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    """Full CRUD endpoint with read vs write permission rules."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedReadOnlyOrAdminWrite]
