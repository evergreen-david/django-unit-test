from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField('Author', through = 'AuthorBook')

    class Meta:
        db_table = 'books'

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    class Meta:
        db_table = 'authors'

class AuthorBook(models.Model):
    book = models.ForeignKey('Book', on_delete= models.SET_NULL, null=True)
    author = models.ForeignKey('Author', on_delete= models.SET_NULL, null=True)

    class Meta:
        db_table = 'author_book'
