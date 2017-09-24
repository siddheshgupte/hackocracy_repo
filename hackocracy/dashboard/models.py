from __future__ import unicode_literals
import json
from django.db import models
from django.conf import settings
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save



# Create your models here.
# class Transactions(models.Model):
#     to = models.CharField(max_length=60)
#     fro = models.CharField(max_length=60)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __unicode__(self):
#         return ' {} -> {} : {} at {} '.format(self.fro, self.to, self.amount, self.timestamp )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    political_party = models.CharField(max_length=50)
    party_image = models.ImageField(upload_to='users/party_logo/',
                                    blank=True)

    def __unicode__(self):
        return 'Profile for user {}'.format(self.user.username)


class Exchanges(models.Model):
    to = models.CharField(max_length=60)
    fro = models.CharField(max_length=60)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return ' {} -> {} : {} at {} '.format(self.fro, self.to, self.amount, self.timestamp )

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


@receiver(pre_save, sender=Exchanges)
def date_handler(sender,instance,*args,**kwargs):
    instance.date = instance.timestamp.isoformat()