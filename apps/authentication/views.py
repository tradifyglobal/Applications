from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Group, User
from .serializers import GroupSerializer, UserSerializer


class StandardPagination(PageNumberPagination):
    page_size = 50


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = StandardPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagination
