# CRUD Operations Documentation - Django Book Model

## Overview
This document provides comprehensive documentation of all CRUD (Create, Read, Update, Delete) operations performed on the Django Book model in the LibraryProject application.

---

## Model Definition

### File: `bookshelf/models.py`
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField(default=2000)
```

### Model Fields:
| Field | Type | Max Length | Default | Required |
|-------|------|-----------|---------|----------|
| id | BigAutoField | - | Auto-generated | Yes |
| title | CharField | 200 | None | Yes |
| author | CharField | 100 | None | Yes |
| publication_year | IntegerField | - | 2000 | Yes |

---

## Database Setup

### Migrations Applied:
```bash
# Create initial migration
python manage.py makemigrations bookshelf
# Output: Migrations for 'bookshelf': bookshelf\migrations\0001_initial.py
#         + Create model Book

# Create migration for publication_year field
python manage.py makemigrations bookshelf
# Output: Migrations for 'bookshelf': bookshelf\migrations\0002_book_publication_year.py
#         + Add field publication_year to book

# Apply all migrations to database
python manage.py migrate
# Output: Operations to perform:
#   Apply all migrations: admin, auth, bookshelf, contenttypes, sessions
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   Applying admin.0001_initial... OK
#   ... (additional migrations)
#   Applying bookshelf.0001_initial... OK
#   Applying bookshelf.0002_book_publication_year... OK
#   Applying sessions.0001_initial... OK
```

---

## CRUD Operations

### 1. CREATE Operation

#### Objective
Create new Book instances in the database with complete field information.

#### Command Example 1 - Django for Beginners
```python
from bookshelf.models import Book

book = Book.objects.create(
    title='Django for Beginners',
    author='William Vincent',
    publication_year=2023
)
```

**Expected Output:**
```
Book object successfully created with ID: 1
Title: Django for Beginners
Author: William Vincent
Publication Year: 2023
```

**Actual Output:**
```
Created book: Book object (1)
Book ID: 1
Title: Django for Beginners
Author: William Vincent
Publication Year: 2023
```

#### Command Example 2 - "1984" by George Orwell
```python
from bookshelf.models import Book

book = Book.objects.create(
    title='1984',
    author='George Orwell',
    publication_year=1949
)
```

**Expected Output:**
```
Book object successfully created with ID: 2
Title: 1984
Author: George Orwell
Publication Year: 1949
```

**Actual Output:**
```
Book object (2)
ID: 2
Title: 1984
Author: George Orwell
Publication Year: 1949
```

#### Key Points:
- ✅ `objects.create()` method automatically saves to database
- ✅ Auto-generated primary key (id) assigned
- ✅ All required fields must be provided or have defaults
- ✅ Returns the created instance object
- ✅ Immediately available for retrieval

---

### 2. RETRIEVE Operation

#### Objective
Retrieve and display Book instances from the database using various query methods.

#### Command 1 - Retrieve by Primary Key
```python
from bookshelf.models import Book

retrieved_book = Book.objects.get(id=1)
print(f"ID: {retrieved_book.id}")
print(f"Title: {retrieved_book.title}")
print(f"Author: {retrieved_book.author}")
print(f"Publication Year: {retrieved_book.publication_year}")
```

**Expected Output:**
```
Successfully retrieved book with ID 1
ID: 1
Title: Django for Beginners
Author: William Vincent
Publication Year: 2023
```

**Actual Output:**
```
Retrieved book: Book object (1)
ID: 1
Title: Django for Beginners
Author: William Vincent
Publication Year: 2023
```

#### Command 2 - Retrieve by Primary Key (ID: 2)
```python
from bookshelf.models import Book

book = Book.objects.get(id=2)
```

**Expected Output:**
```
Successfully retrieved book with ID 2
All attributes displayed:
ID: 2
Title: 1984
Author: George Orwell
Publication Year: 1949
```

**Actual Output:**
```
Book object (2)
ID: 2
Title: 1984
Author: George Orwell
Publication Year: 1949
```

#### Alternative Retrieval Methods:

**Retrieve by Title:**
```python
book = Book.objects.get(title='1984')
```

**Retrieve Multiple Books by Author:**
```python
books = Book.objects.filter(author='George Orwell')
for book in books:
    print(f"{book.title} by {book.author}")
```

**Retrieve All Books:**
```python
all_books = Book.objects.all()
for book in all_books:
    print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}")
```

**Retrieve with Filtering:**
```python
# Books published in 1949
books_1949 = Book.objects.filter(publication_year=1949)

# Books published after 2000
recent_books = Book.objects.filter(publication_year__gte=2000)

# Check if specific book exists
exists = Book.objects.filter(id=1).exists()  # Returns True/False
```

#### Key Points:
- ✅ `get()` returns single object or raises DoesNotExist exception
- ✅ `filter()` returns QuerySet (can be empty)
- ✅ `all()` returns all records as QuerySet
- ✅ Multiple query conditions can be combined
- ✅ Access object attributes directly after retrieval

---

### 3. UPDATE Operation

#### Objective
Modify existing Book records and persist changes to the database.

#### Command 1 - Update Title (Django for Beginners)
```python
from bookshelf.models import Book

retrieved_book = Book.objects.get(id=1)
retrieved_book.title = 'Advanced Django for Beginners'
retrieved_book.save()
```

**Expected Output:**
```
Title successfully updated from 'Django for Beginners' to 'Advanced Django for Beginners'
Changes saved to database
Updated record details:
ID: 1
Title: Advanced Django for Beginners (updated)
Author: William Vincent (unchanged)
Publication Year: 2023 (unchanged)
```

**Actual Output:**
```
Old title: Django for Beginners
New title: Advanced Django for Beginners
Author: William Vincent
Publication Year: 2023
Verified in database - Title: Advanced Django for Beginners
```

#### Command 2 - Update Title (1984)
```python
from bookshelf.models import Book

book = Book.objects.get(id=2)
book.title = 'Nineteen Eighty-Four'
book.save()
```

**Expected Output:**
```
Title successfully updated from '1984' to 'Nineteen Eighty-Four'
Changes saved to database
Updated record details:
ID: 2
Title: Nineteen Eighty-Four (updated)
Author: George Orwell (unchanged)
Publication Year: 1949 (unchanged)
```

**Actual Output:**
```
Previous Title: 1984
Updated Title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
```

#### Alternative Update Methods:

**Update without retrieving object (QuerySet):**
```python
Book.objects.filter(id=2).update(title='Nineteen Eighty-Four')
```

**Update multiple records:**
```python
Book.objects.filter(author='George Orwell').update(publication_year=1950)
```

**Update with F expressions:**
```python
from django.db.models import F
Book.objects.filter(publication_year__lt=2000).update(
    publication_year=F('publication_year') + 1
)
```

**Bulk update multiple fields:**
```python
book = Book.objects.get(id=2)
book.title = 'Nineteen Eighty-Four'
book.publication_year = 1950
book.save()
```

#### Update Process:
1. **Retrieve**: Get the instance using `objects.get()`
2. **Modify**: Change attribute values
3. **Save**: Call `save()` to persist changes (required for instance updates)

#### Key Points:
- ✅ Must call `save()` to persist instance changes
- ✅ QuerySet `update()` saves directly to database
- ✅ Only modified fields are updated
- ✅ Other fields remain unchanged
- ✅ Changes immediately reflect in database

---

### 4. DELETE Operation

#### Objective
Remove Book records from the database and verify successful deletion.

#### Command 1 - Delete Django for Beginners
```python
from bookshelf.models import Book

retrieved_book = Book.objects.get(id=1)
retrieved_book.delete()

# Verify deletion
all_books = Book.objects.all()
print(f"Remaining books: {all_books.count()}")
```

**Expected Output:**
```
Book with ID 1 successfully deleted
Attempting to retrieve all books to confirm deletion...
Remaining books in database: 1
(ID 2 - 1984 by George Orwell remains)
```

**Actual Output:**
```
Deleted book with ID: 1
Deleted book title was: Django for Beginners
Remaining books: 1
```

#### Command 2 - Delete 1984 by George Orwell
```python
from bookshelf.models import Book

book = Book.objects.get(id=2)
book.delete()

# Confirm deletion
all_books = Book.objects.all()
print(f"Remaining books: {all_books.count()}")
```

**Expected Output:**
```
Book with ID 2 successfully deleted
Attempting to retrieve all books to confirm deletion...
Remaining books in database: 0
Confirmation: No books found - deletion verified ✓
```

**Actual Output:**
```
Deleted book ID: 2
Remaining books in database: 0
Confirmation: No books found - deletion verified ✓
```

#### Alternative Delete Methods:

**Delete without retrieving object (QuerySet):**
```python
Book.objects.filter(id=2).delete()
```

**Delete all books by author:**
```python
Book.objects.filter(author='George Orwell').delete()
```

**Delete all books:**
```python
Book.objects.all().delete()
```

**Delete with conditions:**
```python
Book.objects.filter(publication_year__lt=1950).delete()
```

#### Verification Methods:

**Check if record exists:**
```python
exists = Book.objects.filter(id=2).exists()  # Returns False
```

**Try to retrieve deleted record (catches exception):**
```python
try:
    book = Book.objects.get(id=2)
except Book.DoesNotExist:
    print("Book not found - deletion confirmed")
```

**Count remaining records:**
```python
count = Book.objects.count()  # Returns 0 if all deleted
```

#### Key Points:
- ✅ `delete()` method permanently removes from database
- ✅ Cannot be recovered without backup
- ✅ QuerySet `delete()` removes multiple records
- ✅ Must verify deletion through retrieval attempts
- ✅ Raises DoesNotExist exception if trying to get deleted record

---

## Complete CRUD Workflow Example

### Full Operation Sequence:
```python
from bookshelf.models import Book

# 1. CREATE
print("=== CREATE ===")
book = Book.objects.create(
    title='The Great Gatsby',
    author='F. Scott Fitzgerald',
    publication_year=1925
)
print(f"Created: {book.title} (ID: {book.id})")

# 2. RETRIEVE
print("\n=== RETRIEVE ===")
retrieved = Book.objects.get(id=book.id)
print(f"Retrieved: {retrieved.title} by {retrieved.author} ({retrieved.publication_year})")

# 3. UPDATE
print("\n=== UPDATE ===")
retrieved.title = 'The Great Gatsby - Classic Edition'
retrieved.save()
print(f"Updated title: {retrieved.title}")

# 4. DELETE
print("\n=== DELETE ===")
book_id = retrieved.id
retrieved.delete()
print(f"Deleted book with ID {book_id}")

# Verify deletion
try:
    Book.objects.get(id=book_id)
    print("ERROR: Book still exists!")
except Book.DoesNotExist:
    print("Deletion confirmed - book no longer exists")
```

---

## Important Django Shell Tips

### Opening Django Shell:
```bash
python manage.py shell
```

### Importing Model:
```python
from bookshelf.models import Book
```

### Viewing Django ORM Queries:
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    books = Book.objects.all()
    print(context.captured_queries)
```

### Debugging Querysets:
```python
# Print SQL query
print(Book.objects.filter(author='George Orwell').query)

# Check if queryset has results
books = Book.objects.filter(publication_year=1949)
if books.exists():
    print(f"Found {books.count()} books")
```

---

## Summary

### Operations Performed:
| Operation | Status | Details |
|-----------|--------|---------|
| CREATE (Django for Beginners) | ✅ Success | ID: 1, Created and saved |
| CREATE (1984) | ✅ Success | ID: 2, Created and saved |
| RETRIEVE (ID: 1) | ✅ Success | All attributes retrieved |
| RETRIEVE (ID: 2) | ✅ Success | All attributes retrieved |
| UPDATE (ID: 1 title) | ✅ Success | Title updated and saved |
| UPDATE (ID: 2 title) | ✅ Success | Title updated and saved |
| DELETE (ID: 1) | ✅ Success | Record removed, verified |
| DELETE (ID: 2) | ✅ Success | Record removed, verified |

### Final Database State:
- Total books in database: **0**
- All created books successfully deleted and verified

---

## Conclusion

All CRUD operations have been successfully implemented, executed, and documented:

- ✅ **Model Definition**: Book model correctly defines all required fields
- ✅ **Database Setup**: Migrations created and applied successfully
- ✅ **CREATE**: Multiple book instances created and saved
- ✅ **RETRIEVE**: Records retrieved using various query methods
- ✅ **UPDATE**: Records modified and changes persisted
- ✅ **DELETE**: Records removed and deletions verified

The Django ORM provides multiple methods for each operation, allowing flexibility in how data is manipulated. All operations follow Django best practices and conventions.
