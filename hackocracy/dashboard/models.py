from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    political_party = models.CharField(max_length=50)
    party_image = models.ImageField(upload_to='users/party_logo/',
                                    blank=True)

    def __unicode__(self):
        return 'Profile for user {}'.format(self.user.username)