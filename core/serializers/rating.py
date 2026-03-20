from rest_framework import serializers

from core.models import Rating

class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'book', 'note', 'comment']
