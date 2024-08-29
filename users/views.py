from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import UsersPermission
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    permission_classes = [UsersPermission | IsAuthenticated & IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
