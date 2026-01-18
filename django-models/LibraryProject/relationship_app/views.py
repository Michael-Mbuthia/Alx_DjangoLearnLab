from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Library


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
