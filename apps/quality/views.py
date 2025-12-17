from rest_framework import viewsets
from .models import QualityCheck
from .serializers import QualityCheckSerializer


class QualityCheckViewSet(viewsets.ModelViewSet):
    queryset = QualityCheck.objects.all()
    serializer_class = QualityCheckSerializer
    filterset_fields = ['status', 'check_date']
