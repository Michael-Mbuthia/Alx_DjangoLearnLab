# CREATE Operation - "1984" by George Orwell

## Objective
Create a Book instance with the title "1984", author "George Orwell", and publication year 1949.

## Python Command
```python
from bookshelf.models import Book

book = Book.objects.create(
    title='1984',
    author='George Orwell',
    publication_year=1949
)
```

## Expected Output
```
# Book object successfully created with ID: 2
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
# The create() method automatically saves the instance to the database
# and returns the created object with an auto-generated primary key.
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
>>> book = Book.objects.create(
...     title='1984',
...     author='George Orwell',
...     publication_year=1949
... )
# Output: Book object with ID 2 created and saved to database
>>> print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
# Output: ID: 2, Title: 1984, Author: George Orwell, Year: 1949
```

## Key Points
- ✅ Book instance created successfully
- ✅ Auto-generated primary key (ID: 2)
- ✅ All fields populated correctly
- ✅ Automatically saved to database
- ✅ Ready for retrieval and further operations

## Status
✅ **Successfully created Book instance with ID 2**
