from django.db import models
from django.core.validators import RegexValidator


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    isbn_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^(?:\d{10}|\d{13})$',
                message='ISBN must be 10 or 13 digits long.'
            )
        ]
    )
    number_of_pages = models.PositiveIntegerField()
    cover_link = models.URLField()
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ka', 'Georgian'),
        ('pt', 'Portuguese'),
        ('fr', 'French'),
        ('es', 'Spanish'),
        ('it', 'Italian'),
        ('de', 'German'),
    ]
    publication_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return self.title
