from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets

from taggit.forms import TagWidget

from .models import Comment, Post, Tag

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=TagWidget(),
        help_text="Comma-separated tags (e.g. django, web, python)",
    )

    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            'content': widgets.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            existing = self.instance.tags.order_by('name').values_list('name', flat=True)
            self.fields['tags'].initial = ", ".join(existing)

    def save(self, commit=True):
        post = super().save(commit=commit)

        raw_tags = (self.cleaned_data.get('tags') or '').strip()
        if commit:
            tag_names = [t.strip() for t in raw_tags.split(',') if t.strip()]
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            post.tags.set(tags)
        return post


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ("content",)
