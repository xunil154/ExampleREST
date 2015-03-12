from django.db import models
from django.conf import settings

class Note(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notes')
    subject = models.CharField(max_length=100)
    note = models.TextField(blank=True,null=True)
