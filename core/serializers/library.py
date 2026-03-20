from rest_framework import serializers

from core.models import Library

class LibrarySerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        source='book_set',
        many=True,
        read_only=True,
        view_name='book-detail'
    )

    class Meta:
        model = Library
        fields = ['id', 'user', 'books']
