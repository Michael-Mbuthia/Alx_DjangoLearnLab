from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from .models import Book
from .models import Library
from .models import Author


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


# ============================================================================
# ROLE-BASED ACCESS CONTROL: Helper Functions
# ============================================================================
def is_admin(user):
    """
    Check if user has Admin role.
    
    Args:
        user: Django User object
        
    Returns:
        Boolean indicating if user is Admin
    """
    return hasattr(user, 'profile') and user.profile.role == 'Admin'


def is_librarian(user):
    """
    Check if user has Librarian role.
    
    Args:
        user: Django User object
        
    Returns:
        Boolean indicating if user is Librarian
    """
    return hasattr(user, 'profile') and user.profile.role == 'Librarian'


def is_member(user):
    """
    Check if user has Member role.
    
    Args:
        user: Django User object
        
    Returns:
        Boolean indicating if user is Member
    """
    return hasattr(user, 'profile') and user.profile.role == 'Member'


# ============================================================================
# ROLE-BASED VIEWS: Admin, Librarian, and Member Views
# ============================================================================
@login_required(login_url='relationship_app:login')
@user_passes_test(is_admin)
def admin_view(request):
    """
    Admin-only view that displays admin dashboard and statistics.
    Only users with 'Admin' role can access this view.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered admin template with admin-specific content
    """
    total_books = Book.objects.count()
    total_libraries = Library.objects.count()
    total_authors = Author.objects.count()
    
    context = {
        'total_books': total_books,
        'total_libraries': total_libraries,
        'total_authors': total_authors,
        'user_role': request.user.profile.role,
    }
    return render(request, 'relationship_app/admin_view.html', context)


@login_required(login_url='relationship_app:login')
@user_passes_test(is_librarian)
def librarian_view(request):
    """
    Librarian-only view that displays librarian dashboard.
    Only users with 'Librarian' role can access this view.
    Displays library management tools and book statistics.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered librarian template with librarian-specific content
    """
    libraries = Library.objects.all()
    books = Book.objects.all()
    
    context = {
        'libraries': libraries,
        'books': books,
        'total_libraries': libraries.count(),
        'total_books': books.count(),
        'user_role': request.user.profile.role,
    }
    return render(request, 'relationship_app/librarian_view.html', context)


@login_required(login_url='relationship_app:login')
@user_passes_test(is_member)
def member_view(request):
    """
    Member-only view that displays member dashboard.
    Only users with 'Member' role can access this view.
    Displays available books and libraries for browsing.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered member template with member-specific content
    """
    books = Book.objects.all()
    libraries = Library.objects.all()
    
    context = {
        'books': books,
        'libraries': libraries,
        'total_books': books.count(),
        'total_libraries': libraries.count(),
        'user_role': request.user.profile.role,
    }
    return render(request, 'relationship_app/member_view.html', context)
