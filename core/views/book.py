from rest_framework import viewsets

from core.models import Book
from core.serializers import BookSerializer
from core.utils.query import get_query_all_for_user

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return get_query_all_for_user(Book, self.request.user).order_by('id')
