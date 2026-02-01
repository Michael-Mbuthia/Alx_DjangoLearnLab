from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from .models import Book
from .forms import ExampleForm


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
	# Security notes:
	# - Permission enforcement is done server-side via permission_required.
	# - This view only reads data via the ORM (no raw SQL).
	books = Book.objects.all()
	return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_view', raise_exception=True)
def book_search(request):
	"""Search books safely.

	Security notes:
	- Validates input via ExampleForm (no trust in raw querystring).
	- Uses Django ORM lookups (parameterized) instead of string-built SQL.
	"""
	form = ExampleForm(request.GET)
	books = Book.objects.all()
	query = ''

	if form.is_valid():
		query = (form.cleaned_data.get('query') or '').strip()
		if query:
			books = books.filter(
				Q(title__icontains=query) |
				Q(author__icontains=query)
			)

	return render(
		request,
		'bookshelf/book_list.html',
		{'books': books, 'form': form, 'query': query},
	)
