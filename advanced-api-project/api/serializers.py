"""api.serializers

Serializer layer for the Author/Book models.

Purpose:
    Django REST Framework (DRF) serializers translate model instances to
    primitive Python datatypes (and back), which are then rendered as JSON.

Relationship handling (Author -> Book):
    - Book has a ForeignKey to Author (`Book.author`).
    - Author therefore has a reverse relation to all books.
    - Because we set `related_name='books'` on the ForeignKey, the reverse
      accessor is `author.books`.

    `AuthorSerializer` uses a nested `BookSerializer` to dynamically include
    an author's related books in the serialized representation.
"""

from __future__ import annotations

from django.utils import timezone
from rest_framework import serializers

from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """Serializes Book instances.

    Requirements:
        - Must serialize all fields of the Book model.
        - Must reject publication years set in the future.

    Validation:
        We validate `publication_year` at the serializer level to ensure API
        inputs cannot create logically invalid records.
    """

    class Meta:
        model = Book
        fields = "__all__"

    def validate_publication_year(self, value: int) -> int:
        """Ensure `publication_year` is not greater than the current year."""

        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (max {current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author instances, nesting related books.

    Fields:
        - name: the author's name.
        - books: nested list of this author's books.

    Notes:
        `books` is read-only here; book creation/update is expected to happen
        using BookSerializer.
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["name", "books"]
