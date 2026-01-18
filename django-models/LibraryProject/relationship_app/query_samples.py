"""
Sample queries demonstrating complex relationships in Django ORM.
This script demonstrates ForeignKey, ManyToMany, and OneToOne relationships.
"""
# type: ignore

from .models import Author, Book, Library, Librarian


# ============================================================================
# QUERY 1: Query all books by a specific author
# ============================================================================
def get_books_by_author(author_id):
    """
    Retrieve all books written by a specific author using ForeignKey.
    
    Args:
        author_id: The ID of the author
        
    Returns:
        QuerySet of Book objects by the specified author
    """
    try:
        author = Author.objects.get(id=author_id)
        books = author.books.all()  # Using reverse relation (related_name='books')
        print(f"\nBooks by {author.name}:")
        for book in books:
            print(f"  - {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author with ID {author_id} not found.")
        return None


# Alternative method using filter on Book model
def get_books_by_author_alt(author_id):
    """
    Alternative method: Query books using filter on Book model.
    
    Args:
        author_id: The ID of the author
        
    Returns:
        QuerySet of Book objects by the specified author
    """
    books = Book.objects.filter(author_id=author_id)
    print(f"\nBooks by author (ID: {author_id}):")
    for book in books:
        print(f"  - {book.title} by {book.author.name}")
    return books


# ============================================================================
# QUERY 2: List all books in a library
# ============================================================================
def get_books_in_library(library_id):
    """
    Retrieve all books in a specific library using ManyToMany relationship.
    
    Args:
        library_id: The ID of the library
        
    Returns:
        QuerySet of Book objects in the specified library
    """
    try:
        library = Library.objects.get(id=library_id)
        books = library.books.all()  # Using ManyToMany relation
        print(f"\nBooks in {library.name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library with ID {library_id} not found.")
        return None


def get_books_in_library_by_name(library_name):
    """
    Retrieve all books in a specific library by library name.
    Alternative method using library name instead of ID.
    
    Args:
        library_name: The name of the library
        
    Returns:
        QuerySet of Book objects in the specified library
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Using ManyToMany relation
        print(f"\nBooks in {library.name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library with name '{library_name}' not found.")
        return None


# Alternative method using filter on Book through ManyToMany
def get_libraries_for_book(book_id):
    """
    Reverse query: Find all libraries that have a specific book.
    
    Args:
        book_id: The ID of the book
        
    Returns:
        QuerySet of Library objects containing the specified book
    """
    try:
        book = Book.objects.get(id=book_id)
        libraries = book.libraries.all()  # Using reverse relation (related_name='libraries')
        print(f"\nLibraries containing '{book.title}':")
        for library in libraries:
            print(f"  - {library.name}")
        return libraries
    except Book.DoesNotExist:
        print(f"Book with ID {book_id} not found.")
        return None


# ============================================================================
# QUERY 3: Retrieve the librarian for a library
# ============================================================================
def get_librarian_for_library(library_id):
    """
    Retrieve the librarian for a specific library using OneToOne relationship.
    
    Args:
        library_id: The ID of the library
        
    Returns:
        Librarian object associated with the specified library
    """
    try:
        library = Library.objects.get(id=library_id)
        librarian = library.librarian  # Using OneToOne relation
        print(f"\nLibrarian of {library.name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library with ID {library_id} not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library.name}.")
        return None


# Alternative method using filter on Librarian model
def get_library_for_librarian(librarian_id):
    """
    Reverse query: Find the library managed by a specific librarian.
    
    Args:
        librarian_id: The ID of the librarian
        
    Returns:
        Library object managed by the specified librarian
    """
    try:
        librarian = Librarian.objects.get(id=librarian_id)
        library = librarian.library  # Using OneToOne relation
        print(f"\nLibrary managed by {librarian.name}: {library.name}")
        return library
    except Librarian.DoesNotExist:
        print(f"Librarian with ID {librarian_id} not found.")
        return None


# ============================================================================
# ADDITIONAL COMPLEX QUERIES
# ============================================================================
def get_all_authors_with_books_in_library(library_id):
    """
    Get all authors whose books are in a specific library.
    Demonstrates chaining relationships.
    
    Args:
        library_id: The ID of the library
        
    Returns:
        QuerySet of Author objects
    """
    try:
        library = Library.objects.get(id=library_id)
        # Using distinct() to avoid duplicates if an author has multiple books
        authors = Author.objects.filter(books__libraries=library).distinct()
        print(f"\nAuthors in {library.name}:")
        for author in authors:
            print(f"  - {author.name}")
        return authors
    except Library.DoesNotExist:
        print(f"Library with ID {library_id} not found.")
        return None


def get_library_info(library_id):
    """
    Get comprehensive information about a library including librarian and books.
    
    Args:
        library_id: The ID of the library
        
    Returns:
        Dictionary containing library information
    """
    try:
        library = Library.objects.get(id=library_id)
        librarian = library.librarian
        books = library.books.all()
        
        info = {
            'library_name': library.name,
            'librarian_name': librarian.name,
            'total_books': books.count(),
            'books': [book.title for book in books]
        }
        
        print("--- Library Info ---")
        print(f"Library: {info['library_name']}")
        print(f"Librarian: {info['librarian_name']}")
        print(f"Total Books: {info['total_books']}")
        print(f"Books: {', '.join(info['books']) if info['books'] else 'None'}")
        
        return info
    except Library.DoesNotExist:
        print(f"Library with ID {library_id} not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to library ID {library_id}.")
        return None


# ============================================================================
# SAMPLE USAGE (Uncomment to use in Django shell)
# ============================================================================
"""
# To use these queries, open Django shell:
# python manage.py shell

# Then import and run:
# from relationship_app.query_samples import *

# Example queries:
# get_books_by_author(1)
# get_books_by_author_alt(1)
# get_books_in_library(1)
# get_libraries_for_book(1)
# get_librarian_for_library(1)
# get_library_for_librarian(1)
# get_all_authors_with_books_in_library(1)
# get_library_info(1)
"""
