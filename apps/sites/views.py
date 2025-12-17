from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Site
from .serializers import SiteSerializer


class StandardPagination(PageNumberPagination):
    page_size = 50


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    pagination_class = StandardPagination
