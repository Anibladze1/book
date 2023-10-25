from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
                  'isbn_number',
                  'title',
                  'author',
                  'publication_date',
                  'number_of_pages',
                  'cover_link',
                  'publication_language']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'})
        }


class ImportBooksForm(forms.Form):
    keywords = forms.CharField(label='Import by keyword', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter keywords'}))