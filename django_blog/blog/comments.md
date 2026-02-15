# Comment System

This app supports comments on posts with create/update/delete operations and author-only permissions.

## Model

Defined in [blog/models.py](blog/models.py):

- `Comment.post` — ForeignKey to `Post` (many comments per post)
- `Comment.author` — ForeignKey to Django `User`
- `Comment.content` — comment text
- `Comment.created_at` — set on create
- `Comment.updated_at` — updated on every save

## URLs

Defined in [blog/urls.py](blog/urls.py):

- Create (nested): `/posts/<int:post_id>/comments/new/` (login required)
- Edit: `/comments/<int:pk>/edit/` (author only)
- Delete: `/comments/<int:pk>/delete/` (author only)

## Views + permissions

Implemented in [blog/views.py](blog/views.py):

- `CommentCreateView` uses `LoginRequiredMixin` and automatically sets `author` + `post`.
- `CommentUpdateView` and `CommentDeleteView` use `UserPassesTestMixin` to restrict actions to the comment author.

## Templates

- Comments are displayed on the post detail page: [blog/templates/blog/post_detail.html](blog/templates/blog/post_detail.html)
- Edit: [blog/templates/blog/comment_form.html](blog/templates/blog/comment_form.html)
- Delete confirm: [blog/templates/blog/comment_confirm_delete.html](blog/templates/blog/comment_confirm_delete.html)

All POST forms include `{% csrf_token %}`.

## How to test

Run automated tests:

- `Set-Location C:/Users/jm744/Documents/Alx_DjangoLearnLab/django_blog`
- `C:/Users/jm744/Documents/Alx_DjangoLearnLab/.venv/Scripts/python.exe manage.py test`

Manual checks:

1. Visit a post detail page (`/posts/<pk>/`).
2. Log in and submit a new comment.
3. Confirm edit/delete links appear only for your own comments.
4. Log out (or use another user) and confirm edit/delete returns 403.
