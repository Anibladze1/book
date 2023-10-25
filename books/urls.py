from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('books/', views.BookListView.as_view(), name='books-list'),
    path('books/create/', views.BookCreateView.as_view(), name='books-create'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='books-detail'),
    path('books/<int:pk>/update', views.BookUpdateView.as_view(), name='books-update'),
    path('books/<int:pk>/delete', views.BookDeleteView.as_view(), name='books-delete'),
    path('books/import/', views.BookImportView.as_view(), name='books-import'),
]