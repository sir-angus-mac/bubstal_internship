from django.db import models

class Email(models.Model):
    email_name = models.TextField(blank=False)
    kanban = models.JSONField() 
    def __str__(self):
            return self.email_name