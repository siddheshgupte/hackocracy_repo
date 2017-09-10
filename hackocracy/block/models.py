from __future__ import unicode_literals
import json
from django.db import models

# Create your models here.


class BlockChain(models.Model):
    block = models.TextField(max_length=500)

    def __unicode__(self):
        q = json.loads(self.block)
        # return "This is block number {} with data : {} and hash {}".format(q.index,
        #                                                                    q.data,
        #                                                                    q.hash)

        return self.block