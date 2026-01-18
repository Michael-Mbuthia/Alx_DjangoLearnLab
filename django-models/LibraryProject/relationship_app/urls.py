from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view: List all books
    path('books/', views.list_books, name='list_books'),
    
    # Class-based views: Library-related views
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
