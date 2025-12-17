from django.db import models


class Equipment(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'maintenance_equipment'
        ordering = ['name']

    def __str__(self):
        return self.name


class MaintenanceRequest(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    )
    
    ticket_no = models.CharField(max_length=50, unique=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=(('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'maintenance_request'
        ordering = ['-created_at']

    def __str__(self):
        return self.ticket_no
