from __future__ import unicode_literals

from django.db import models

# Create your models here.
class transactions(models.Model):
    to = models.CharField(max_length=60)
    fro = models.CharField(max_length=60)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)



