from rest_framework import serializers

from core.models import Library
from .book import BookSerializer

class LibrarySerializer(serializers.HyperlinkedModelSerializer):
    books = BookSerializer(source='book_set', many=True, read_only=True)

    class Meta:
        model = Library
        fields = ['id', 'user', 'books']
