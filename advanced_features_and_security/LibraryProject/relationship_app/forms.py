from django import forms
from django.core.exceptions import ValidationError

from .models import Author


class BookInputForm(forms.Form):
    """Validates user input for creating/updating a Book.

    Uses Django's validation system to avoid trusting raw request.POST values.
    """

    title = forms.CharField(max_length=300, required=True)
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=True)

    def clean_title(self):
        title = (self.cleaned_data.get('title') or '').strip()
        if not title:
            raise ValidationError('Title is required.')
        return title
