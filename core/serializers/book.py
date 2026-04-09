from rest_framework import serializers

from core.models import Book
from .author import AuthorSerializer

class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover_url', 'author', 'isbn', 'language', 'pages', 'published', 'resume']
