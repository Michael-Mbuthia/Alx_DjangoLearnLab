from django import forms
from django.core.exceptions import ValidationError

from .models import Author


class BookInputForm(forms.Form):
    """Validates user input for creating/updating a Book.

        Security notes:
        - We validate and normalize input (e.g., stripping title) instead of trusting
            raw request.POST values.
        - author is a ModelChoiceField, so an attacker cannot inject arbitrary SQL
            via an "author" parameter; Django ORM performs safe parameterization.
    """

    title = forms.CharField(max_length=300, required=True)
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=True)

    def clean_title(self):
        title = (self.cleaned_data.get('title') or '').strip()
        if not title:
            raise ValidationError('Title is required.')
        return title
