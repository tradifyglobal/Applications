from rest_framework import viewsets
from .models import Equipment, MaintenanceRequest
from .serializers import EquipmentSerializer, MaintenanceRequestSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    search_fields = ['name', 'code', 'location']


class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    filterset_fields = ['status', 'priority', 'equipment']
    search_fields = ['ticket_no']
