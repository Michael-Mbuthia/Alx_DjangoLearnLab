# Authentication System (django_blog)

This project uses Django’s built-in authentication views for **login** and **logout**, and custom views for **registration** and **profile management**.

## URL routes

These routes are defined in [blog/urls.py](blog/urls.py) and included at the project root by [django_blog/urls.py](django_blog/urls.py):

- `/login/` — built-in `LoginView`
- `/logout/` — built-in `LogoutView`
- `/register/` — custom registration view
- `/profile/` — custom profile view (requires login)

## Forms

Defined in [blog/forms.py](blog/forms.py):

- `UserRegistrationForm`
  - Extends `UserCreationForm`
  - Adds an `email` field (required)
- `UserUpdateForm`
  - Lets an authenticated user update `username`, `first_name`, `last_name`, and `email`

## Views

Defined in [blog/views.py](blog/views.py):

- `register`
  - Displays the registration form
  - On POST: creates the user, stores the email, logs the user in, and redirects to `/profile/`
- `profile`
  - Protected with `@login_required`
  - On POST: updates the user fields (including email)

## Templates

Templates live inside the `blog` app so Django can find them via `APP_DIRS=True`:

- Login: [blog/templates/registration/login.html](blog/templates/registration/login.html)
- Logout: [blog/templates/registration/logout.html](blog/templates/registration/logout.html)
- Registration: [blog/templates/blog/register.html](blog/templates/blog/register.html)
- Profile: [blog/templates/blog/profile.html](blog/templates/blog/profile.html)

All forms include `{% csrf_token %}`.

## Settings

Auth-related settings are in [django_blog/settings.py](django_blog/settings.py):

- `LOGIN_URL = '/login/'`
- `LOGIN_REDIRECT_URL = '/profile/'`
- `LOGOUT_REDIRECT_URL = '/login/'`

## How to test

Run tests:

- `Set-Location C:/Users/jm744/Documents/Alx_DjangoLearnLab/django_blog`
- `C:/Users/jm744/Documents/Alx_DjangoLearnLab/.venv/Scripts/python.exe manage.py test`

Manual test steps:

1. Visit `/register/` and create an account.
2. Confirm you land on `/profile/`.
3. Edit your email and save.
4. Log out.
5. Try visiting `/profile/` again and confirm you are redirected to `/login/`.
