from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# ticket table
class Ticket(models.Model):
    user = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='tickets'
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
        choices=[
            ('Open', 'Open'),
            ('In Progress', 'In Progress'),
            ('Resolved', 'Resolved'),
        ],
        default='Open'
    )

    # IT staff member handling the ticket
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )

    # Feedback or resolution recorded by IT support
    resolution_response = models.TextField(
        blank=True,
        null=True
    )

    # Automatically updated whenever the ticket changes
    updated_at = models.DateTimeField(auto_now=True)

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    # ai_status = models.CharField(
    # max_length=30,
    # default='Pending'
    # )

    # ai_response = models.TextField(
    #     blank=True,
    #     null=True
    # )

    # ai_confidence = models.FloatField(
    #     blank=True,
    #     null=True
    # )

    # ai_reason = models.TextField(
    #     blank=True,
    #     null=True
    # )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.ticket_title
    
# class Artificial_chat(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )
#     ai_chat = models.TextField(
#         blank=True
#     )
#     user_chat = models.TextField(
#         blank=True
#     )
    
#     def __str__(self):
#             return self.ticket_title