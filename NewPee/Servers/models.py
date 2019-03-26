from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=140, null=False, blank=False)
    host = models.CharField(max_length=140, null=False, blank=False)


