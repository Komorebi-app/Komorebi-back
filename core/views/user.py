from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.serializers import UserSerializer, UserRegisterSerializer
from core.utils.query import get_query_all_for_user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["new"]:
            return [AllowAny()]
        if self.action in ["me"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        return get_query_all_for_user(User, self.request.user).order_by('id')

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], serializer_class=UserRegisterSerializer)
    def new(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
