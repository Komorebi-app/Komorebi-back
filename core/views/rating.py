from rest_framework import viewsets

from core.models import Rating
from core.serializers import RatingSerializer
from core.utils.query import get_query_all_for_user

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return get_query_all_for_user(Rating, self.request.user).order_by('id')
