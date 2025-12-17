from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Employee, Attendance, Leave
from .serializers import EmployeeSerializer, AttendanceSerializer, LeaveSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_fields = ['department', 'is_active']
    search_fields = ['first_name', 'last_name', 'employee_id', 'email']


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filterset_fields = ['employee', 'status', 'date']


class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    filterset_fields = ['employee', 'leave_type', 'status']
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        leave.status = 'A'
        leave.approved_by = request.user.employee
        leave.save()
        return Response({'status': 'leave approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        leave = self.get_object()
        leave.status = 'R'
        leave.save()
        return Response({'status': 'leave rejected'})
