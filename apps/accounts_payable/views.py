from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *

class StandardPagination(PageNumberPagination):
    page_size = 50

