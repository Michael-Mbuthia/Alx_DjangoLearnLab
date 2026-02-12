"""api.models

Data layer for the REST API example.

This app models a simple publishing domain with a one-to-many relationship:

- One Author can have many Book records.
- Each Book belongs to exactly one Author.

These models are intentionally minimal so they map cleanly to Django REST
Framework serializers and demonstrate nested serialization.
"""

from django.db import models


class Author(models.Model):
    """Represents a writer.

    Fields:
        name: A string field storing the author's name.

    Relationship:
        Books are linked via `Book.author` (ForeignKey).
        With `related_name='books'`, the reverse relation is:
            author.books.all()
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    """Represents a book written by an Author.

    Fields:
        title: A string field for the book's title.
        publication_year: An integer year the book was published.
        author: ForeignKey linking this book to its Author.

    Notes:
        The "not in the future" rule for publication_year is enforced in the
        REST serializer (see api/serializers.py) so API inputs are validated.
    """

    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
    )

    def __str__(self):
        return str(self.title)
