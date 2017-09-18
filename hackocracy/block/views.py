from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import Exchanges
from block.models import BlockChain
# Create your views here.
import hashlib
from datetime import datetime
import json
import requests
from django.contrib import messages
from decimal import Decimal
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from dashboard.forms import TransactionForm


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


def verify_hash(new_block, json_verify=False):
    if not json_verify:
        calculated_hash = hashlib.sha256(str(new_block.index) +
                                         str(new_block.previous_hash) +
                                         str(new_block.timestamp) +
                                         str(new_block.data)).hexdigest()

        # check if calculated hash is the block's hash
        if calculated_hash == new_block.hash:
            return True
        print('expected hash {} got hash {}'.format(calculated_hash, new_block.hash))
        return False
    calculated_hash = hashlib.sha256(str(new_block['index']) +
                                     str(new_block['previous_hash']) +
                                     str(new_block['timestamp']) +
                                     str(new_block['data'])).hexdigest()
    return calculated_hash


# Check if a chain is valid
# Returns Boolean
# Checks index, previous_hash, hash
def verify_chain(lst):
    prev_index = 0
    prev_hash = '0'
    for ele in lst:
        loaded_ele = json.loads(ele)
        if prev_index != loaded_ele['index']:
            print('index error')
            return False
        if prev_hash != loaded_ele['previous_hash']:
            print('previous hash not equal , expected : {}, got : {}'.format(prev_hash, loaded_ele['previous_hash']))
            return False

        veri_block = Block(loaded_ele['index'], loaded_ele['previous_hash'], loaded_ele['timestamp'],
                           loaded_ele['data'])
        # expected_hash = verify_hash(loaded_ele, json_verify=True)
        if veri_block.hash != loaded_ele['hash']:
            print('expected hash : {} , got {}'.format(veri_block.hash, loaded_ele['hash']))
            return False
        prev_index = loaded_ele['index'] + 1
        prev_hash = loaded_ele['hash']
    return True


def get_peer_blockchains():

    # TODO PEER LIST (Put in settings afterwards)
    peer_list =[]

    list_of_peer_blockchains = []

    for peer in peer_list:
        r = requests.get('http://{}/send_blockchain'.format(peer))
        list_of_peer_blockchains.append(r.json())

    return list_of_peer_blockchains


def consensus(request):

    # Get blocks from other nodes
    list_of_all_blockchains = [request.session['blockchain']]
    list_of_all_blockchains.extend(get_peer_blockchains())

    # Find longest chain and assign it as the current blockchain
    request.session['blockchain'] = max(list_of_all_blockchains, key=len)


@login_required
def mine(request, logging_out=False):

    # Set current blockchain to the largest in the network
    consensus(request)

    print verify_chain(request.session['blockchain'])
    # each node is verifying before sending so this verify may not be needed
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
        Exchanges.objects.all().delete()

    BlockChain.objects.all().delete()
    # Replace with the current blockchain
    for block in request.session['blockchain']:
        q = BlockChain(block=block)
        q.save()
        print 'after mining the session is :'
        print block

    if not logging_out:
        messages.success(request, 'Transactions were made Permanent!')
        return render(request, 'dashboard/Transaction_history.html')





