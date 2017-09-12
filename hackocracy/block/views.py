from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import Exchanges
from block.models import BlockChain
# Create your views here.
import hashlib
from datetime import datetime
import json
from decimal import Decimal
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


def custom_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj.__dict__


class Block:
    def __init__(self, index, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = self.calculate_hash()

    def __unicode__(self):
        return u"This is block number {} with data : {} and hash {}".format(self.index,
                                                                            self.data,
                                                                            self.hash)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def calculate_hash(self):
            return hashlib.sha256(str(self.index) +
                                  str(self.previous_hash) +
                                  str(self.timestamp) +
                                  str(self.data)).hexdigest()

    def toJSON(self):
        return json.dumps(self, default=custom_serializer,
                          sort_keys=True, indent=4, cls=DjangoJSONEncoder)


def get_genesis_block():
    return Block(0, '0', '2017-09-02 23:41:45.944072', 'Genesis block')


def verify_hash(new_block):
    calculated_hash = hashlib.sha256(str(new_block.index) +
                                     str(new_block.previous_hash) +
                                     str(new_block.timestamp) +
                                     str(new_block.data)).hexdigest()

    # check if calculated hash is the block's hash
    if calculated_hash == new_block.hash:
        return True
    print('expected hash {} got hash {}'.format(calculated_hash, new_block.hash))
    return False


# Check if a chain is valid
def is_valid_block(new_block, previous_block):
    if previous_block.index + 1 != new_block.index:
        print('Invalid Index')
        return False
    elif previous_block.hash != new_block.previous_hash:
        print('Invalid previous hash')
        return False
    elif not verify_hash(new_block):
        print('Invalid hash')


@login_required
def mine(request):
    # TODO request peers
    # TODO find largest block
    last_block = json.loads(request.session['blockchain'][-1])

    # set new blocks attributes
    new_block_index = last_block['index'] + 1
    new_block_timestamp = str(datetime.now())
    new_block_previous_hash = last_block['hash']
    new_block_data = []

    # Fetch all from transactions or only user specific...
    q = Exchanges.objects.all()

    if q.exists():

        new_block_data.extend(serializers.serialize('python', q))

        # Make new block and convert to JSON
        new_block = Block(new_block_index,
                          new_block_previous_hash,
                          new_block_timestamp,
                          new_block_data)

        request.session['blockchain'].append(new_block.toJSON())

    # TODO delete the transaction db (only when everything works)

    BlockChain.objects.all().delete()
    # Replace with the current blockchain
    for block in request.session['blockchain']:
        q = BlockChain(block=block)
        q.save()
        print 'after mining the session is :'
        print block




