from django.db import models


class WorkOrder(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    work_order_no = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'production_work_order'
        ordering = ['-created_at']

    def __str__(self):
        return self.work_order_no
