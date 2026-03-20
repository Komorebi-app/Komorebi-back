from rest_framework import serializers

from core.models import Book

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'language', 'pages', 'published', 'resume']
