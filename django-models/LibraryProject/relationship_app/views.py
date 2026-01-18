from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Book
from .models import Library


# ============================================================================
# FUNCTION-BASED VIEW: List all books
# ============================================================================
def list_books(request):
    """
    Function-based view that lists all books in the database.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered template with all books
    """
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


# ============================================================================
# CLASS-BASED VIEW: Library Detail
# ============================================================================
class LibraryDetailView(DetailView):
    """
    Class-based view using Django's DetailView to display library details.
    Shows a specific library and all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


class LibraryListView(ListView):
    """
    Class-based view using Django's ListView to display all libraries.
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'


# ============================================================================
# AUTHENTICATION VIEWS: User Login, Logout, and Registration
# ============================================================================
class UserLoginView(LoginView):
    """
    Class-based view for user login using Django's built-in LoginView.
    Handles user authentication and session management.
    """
    template_name = 'relationship_app/login.html'
    success_url = reverse_lazy('relationship_app:list_books')
    
    def get_success_url(self):
        """Redirect to list_books after successful login."""
        return reverse_lazy('relationship_app:list_books')


class UserLogoutView(LogoutView):
    """
    Class-based view for user logout using Django's built-in LogoutView.
    Clears user session and redirects to logout page.
    """
    template_name = 'relationship_app/logout.html'
    next_page = reverse_lazy('relationship_app:login')


def register_user(request):
    """
    Function-based view for user registration.
    Handles user account creation using Django's UserCreationForm.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered template with registration form or redirect to login
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:login')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'relationship_app/register.html', context)
