"""api.serializers

Serializers define how model instances are translated to/from primitive Python
types (which then become JSON in API responses).

This module demonstrates:

- A flat serializer for Book that includes *all* model fields.
- A nested serializer for Author that includes related Book objects.

Relationship handling:

The `Book.author` field is a ForeignKey to Author (many-to-one).
Django automatically provides a reverse relation from Author to Book.

In `api.models.Book` we set `related_name='books'`, so for an Author instance
`author.books.all()` returns all related books.

`AuthorSerializer` uses that reverse relation and nests `BookSerializer` with
`many=True` and `read_only=True` to dynamically include the author's books in
serialized output.
"""

from __future__ import annotations

from django.utils import timezone
from rest_framework import serializers

from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """Serializes Book instances.

    Requirements:
    - Serializes all fields of the Book model.
    - Validates that publication_year is not in the future.

    Note:
    We enforce the 'not in the future' rule at the serializer layer because it
    is API-input specific validation (as opposed to database constraints).
    """

    class Meta:
        model = Book
        fields = "__all__"

    def validate_publication_year(self, value: int) -> int:
        """Ensure the year is not greater than the current year."""

        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (max {current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author instances, including nested books.

    Output includes:
    - name
    - books: A nested list of Book records for this author.

    The nested books are read-only here; creating/updating books is expected to
    happen through BookSerializer endpoints.
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["name", "books"]
