# RETRIEVE Operation - "1984" by George Orwell

## Objective
Retrieve and display all attributes of the "1984" book previously created.

## Python Command
```python
from bookshelf.models import Book

book = Book.objects.get(id=2)
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

## Expected Output
```
# Successfully retrieved book with ID 2
# All attributes displayed:
# ID: 2
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
```

## Actual Output
```
Book object (2)
ID: 2
Title: 1984
Author: George Orwell
Publication Year: 1949
```

## Code Example with Output
```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(id=2)
>>> book
<Book: Book object (2)>
>>> print(book.id, book.title, book.author, book.publication_year)
# Output: 2 1984 George Orwell 1949
```

## Alternative Retrieval Methods
```python
# Retrieve by title
book = Book.objects.get(title='1984')

# Retrieve by author
books = Book.objects.filter(author='George Orwell')

# Retrieve all books
all_books = Book.objects.all()

# Retrieve with specific publication year
books = Book.objects.filter(publication_year=1949)
```

## Key Points
- ✅ Book retrieved successfully using primary key
- ✅ All attributes accessible and correct
- ✅ Object ready for updates or deletions
- ✅ Multiple query methods available

## Status
✅ **Successfully retrieved Book instance with ID 2**
