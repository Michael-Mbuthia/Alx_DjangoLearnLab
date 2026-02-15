# Tagging & Search

This blog supports tagging posts and searching by title/content/tags.

## Tagging

### Models

Defined in [blog/models.py](blog/models.py):

- `Tag(name)` — unique tag name
- `Post.tags` — `ManyToManyField(Tag, blank=True)`

### Adding tags to posts

The post create/edit form accepts a **comma-separated** list of tags.

Example: `django, python, web`

Implementation is in [blog/forms.py](blog/forms.py) (`PostForm`):

- The `tags` form field is a plain text input.
- On save, any missing tags are created automatically (`Tag.objects.get_or_create`).
- The post’s tags are replaced with the submitted set.

### Viewing posts by tag

URL:

- `/tags/<tag_name>/`

Example:

- `/tags/django/`

## Search

URL:

- `/search/?q=<term>`

Search looks for matches in:

- `Post.title`
- `Post.content`
- `Tag.name` (tags associated with posts)

Search query is implemented with Django `Q` objects in [blog/views.py](blog/views.py) (`PostSearchView`).

## Templates

- The post list page includes a search bar and displays tags: [blog/templates/blog/post_list.html](blog/templates/blog/post_list.html)
- Post detail shows tags and links to tag pages: [blog/templates/blog/post_detail.html](blog/templates/blog/post_detail.html)
- Tag results page: [blog/templates/blog/tag_posts.html](blog/templates/blog/tag_posts.html)
- Search results page: [blog/templates/blog/search_results.html](blog/templates/blog/search_results.html)

## Tests

Tests are in [blog/tests.py](blog/tests.py):

- Creating a post with tags creates missing `Tag` records and assigns them
- Tag filter view returns tagged posts
- Search returns posts matching tag names

Run:

- `Set-Location C:/Users/jm744/Documents/Alx_DjangoLearnLab/django_blog`
- `C:/Users/jm744/Documents/Alx_DjangoLearnLab/.venv/Scripts/python.exe manage.py test`
