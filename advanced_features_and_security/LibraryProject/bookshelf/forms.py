from django import forms
from django.core.exceptions import ValidationError

from .models import Book


class BookForm(forms.ModelForm):
    """Form for creating/updating Book instances.

    Security notes:
    - Uses Django forms validation instead of trusting raw request data.
    - Works with the ORM (no raw SQL), which prevents SQL injection.
    """

    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if not title:
            raise ValidationError("Title is required.")
        return title

    def clean_author(self):
        author = (self.cleaned_data.get("author") or "").strip()
        if not author:
            raise ValidationError("Author is required.")
        return author

    def clean_publication_year(self):
        year = self.cleaned_data.get("publication_year")
        if year is None:
            return year
        if year < 0:
            raise ValidationError("Publication year must be a positive number.")
        return year
