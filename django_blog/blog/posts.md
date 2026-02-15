# Blog Post CRUD Features

This app provides Create/Read/Update/Delete (CRUD) operations for `Post` using Django class-based generic views.

## URLs

Defined in [blog/urls.py](blog/urls.py):

- `/posts/` — list all posts (public)
- `/posts/<int:pk>/` — view a single post (public)
- `/posts/new/` — create a post (login required)
- `/posts/<int:pk>/edit/` — edit a post (author only)
- `/posts/<int:pk>/delete/` — delete a post (author only)

## Views

Implemented in [blog/views.py](blog/views.py):

- `PostListView` (`ListView`) — shows all posts ordered by newest first
- `PostDetailView` (`DetailView`) — shows the full post
- `PostCreateView` (`CreateView`) — uses `LoginRequiredMixin` and automatically sets `author` to the logged-in user
- `PostUpdateView` (`UpdateView`) — `LoginRequiredMixin + UserPassesTestMixin` restricts editing to the author
- `PostDeleteView` (`DeleteView`) — `LoginRequiredMixin + UserPassesTestMixin` restricts deletion to the author

## Form

Defined in [blog/forms.py](blog/forms.py):

- `PostForm` (`ModelForm`) exposes only `title` and `content`.
- `author` is not user-editable; it’s set in `PostCreateView.form_valid`.

## Templates

Located in `blog/templates/blog/`:

- `post_list.html`
- `post_detail.html`
- `post_form.html` (used for create + edit)
- `post_confirm_delete.html`

All POST forms include `{% csrf_token %}`.

## Tests

Defined in [blog/tests.py](blog/tests.py):

- Verifies list/detail are public
- Verifies create requires login and sets `author`
- Verifies non-authors cannot edit/delete

Run:

- `Set-Location C:/Users/jm744/Documents/Alx_DjangoLearnLab/django_blog`
- `C:/Users/jm744/Documents/Alx_DjangoLearnLab/.venv/Scripts/python.exe manage.py test`
