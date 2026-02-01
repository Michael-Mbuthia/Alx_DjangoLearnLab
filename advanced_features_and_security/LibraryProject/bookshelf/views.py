from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from .models import Book


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
	# Security notes:
	# - Permission enforcement is done server-side via permission_required.
	# - This view only reads data via the ORM (no raw SQL).
	books = Book.objects.all()
	return render(request, 'bookshelf/book_list.html', {'books': books})
