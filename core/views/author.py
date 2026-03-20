from rest_framework import viewsets

from core.models import Author
from core.serializers import AuthorSerializer
from core.utils.query import get_query_all_for_user

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        return get_query_all_for_user(Author, self.request.user).order_by('id')
