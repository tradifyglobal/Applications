from django.db import models


class QualityCheck(models.Model):
    STATUS_CHOICES = (
        ('PASSED', 'Passed'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    )
    
    check_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quality_check'
        ordering = ['-check_date']

    def __str__(self):
        return f"Quality Check - {self.check_date}"
