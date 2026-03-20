from rest_framework import viewsets

from core.models import Library
from core.serializers import LibrarySerializer
from core.utils.query import get_query_all_for_user

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return get_query_all_for_user(Library, self.request.user).order_by('id')
