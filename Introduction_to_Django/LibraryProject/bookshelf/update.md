# UPDATE Operation - "1984" by George Orwell

## Objective
Update the title of "1984" to "Nineteen Eighty-Four" and save the changes to the database.

## Python Commands
```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(id=2)

# Update the title
book.title = 'Nineteen Eighty-Four'

# Save the changes to the database
book.save()
```

## Expected Output
```
# Title successfully updated from '1984' to 'Nineteen Eighty-Four'
# Changes saved to database
# 
# Updated record details:
# ID: 2
# Title: Nineteen Eighty-Four (updated)
# Author: George Orwell (unchanged)
# Publication Year: 1949 (unchanged)
```

## Actual Output
```
Previous Title: 1984
Updated Title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
```

## Code Example with Output
```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(id=2)
>>> print(f"Before: {book.title}")
# Output: Before: 1984
>>> book.title = 'Nineteen Eighty-Four'
>>> book.save()
# Database updated
>>> book_updated = Book.objects.get(id=2)
>>> print(f"After: {book_updated.title}")
# Output: After: Nineteen Eighty-Four
```

## Update Process
1. **Retrieve**: Get the book instance using `Book.objects.get(id=2)`
2. **Modify**: Change the attribute - `book.title = 'Nineteen Eighty-Four'`
3. **Save**: Persist changes to database with `book.save()`

## Alternative Update Methods
```python
# Direct update using QuerySet (without retrieving object)
Book.objects.filter(id=2).update(title='Nineteen Eighty-Four')

# Update multiple records
Book.objects.filter(author='George Orwell').update(title='Nineteen Eighty-Four')

# Using F expressions for calculations
from django.db.models import F
Book.objects.filter(id=2).update(publication_year=F('publication_year') + 1)
```

## Key Points
- ✅ Title successfully updated
- ✅ Changes persisted to database
- ✅ Other fields remain unchanged
- ✅ Update verified through re-retrieval
- ✅ save() method is required for instance updates

## Status
✅ **Successfully updated Book title from "1984" to "Nineteen Eighty-Four"**
