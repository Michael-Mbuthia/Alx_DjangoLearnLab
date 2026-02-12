"""api.models

Defines the core data models for this API.

Domain:
    - Author: a person who writes books.
    - Book: a published work written by a single Author.

Relationship:
    This is a classic one-to-many relationship:
        Author (1) -> (many) Book

    Implemented with a ForeignKey on Book pointing to Author.
    The `related_name='books'` enables convenient reverse access:
        author.books.all()
"""

from django.db import models


class Author(models.Model):
    """An author who can have multiple books."""

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.name)


class Book(models.Model):
    """A book written by an Author."""

    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
    )

    def __str__(self) -> str:
        return str(self.title)
