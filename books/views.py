import requests

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from .models import Book, Author
from .forms import BookForm, ImportBooksForm
from .helpers import format_date


class HomeView(TemplateView):
    template_name = 'index.html'


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'create-book.html'
    success_url = reverse_lazy('books-list')


class BookListView(ListView):
    model = Book
    context_object_name = "books"
    template_name = 'book-list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {
            'title__icontains': self.request.GET.get('title'),
            'author__name__icontains': self.request.GET.get('author'),
            'publication_language__icontains': self.request.GET.get('publication_language'),
            'publication_date__year__gte': self.request.GET.get('from_year'),
            'publication_date__year__lte': self.request.GET.get('to_year')
        }
        return queryset.filter(**{k: v for k, v in filters.items() if v})


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = 'book-detail.html'


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'update-book.html'
    success_url = reverse_lazy('books-list')


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('books-list')
    template_name = 'delete-book.html'
    context_object_name = "book"


class BookImportView(FormView):
    template_name = 'import-book.html'
    form_class = ImportBooksForm

    def form_valid(self, form):
        keywords = form.cleaned_data.get('keywords')
        self.import_books_from_google(keywords)
        return redirect('books-list')

    @staticmethod
    def import_books_from_google(keywords):
        url = f'https://www.googleapis.com/books/v1/volumes?q={keywords}'
        response = requests.get(url)
        response.raise_for_status()

        for item in response.json().get('items', []):
            volume_info = item.get('volumeInfo', {})
            author_name = ', '.join(volume_info.get('authors', []))
            author, _ = Author.objects.get_or_create(name=author_name)

            book_data = {
                'title': volume_info.get('title', ''),
                'author': author,
                'publication_date': format_date(volume_info.get('publishedDate', '')),
                'isbn_number': volume_info.get('industryIdentifiers', [{}])[0].get('identifier', ''),
                'number_of_pages': volume_info.get('pageCount', 0),
                'cover_link': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                'publication_language': volume_info.get('language', '')
            }

            Book.objects.create(**book_data)
