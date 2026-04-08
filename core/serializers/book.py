from rest_framework import serializers

from core.models import Book

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'cover_url', 'author', 'isbn', 'language', 'pages', 'published', 'resume']
