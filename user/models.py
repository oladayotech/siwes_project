from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# ticket table
class Ticket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    ticket_code = models.CharField(
        null=True,
        max_length=10
    )

    ticket_title = models.CharField(
        max_length=150
    )

    category = models.CharField(
        max_length=50
    )

    priority = models.CharField(
        max_length=15
    )

    device_type = models.CharField(
        max_length=50
    )

    description = models.TextField()

    attachment = models.FileField(
        upload_to='ticket_attachments/',
        blank=True,
        null=True
    )

    ticket_status = models.CharField(
        max_length=15,
        default='Open'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.ticket_title
    
