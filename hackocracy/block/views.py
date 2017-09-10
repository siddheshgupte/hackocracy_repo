from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
import hashlib
from datetime import datetime
import json


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
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


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


# validate if a block or chain of blocks is valid
# especially when we receive new blocks from other nodes
# we must check those to decide whether to accept them or not
def is_valid_block(new_block, previous_block):
    if previous_block.index + 1 != new_block.index:
        print('Invalid Index')
        return False
    elif previous_block.hash != new_block.previous_hash:
        print('Invalid previous hash')
        return False
    elif not verify_hash(new_block):
        print('Invalid hash')


def generate_next_block(data, last_block):
    next_index = last_block.index + 1
    next_timestamp = datetime.now()
    next_data = data
    next_last_block_hash = last_block.hash
    return Block(next_index, next_last_block_hash.hash, next_timestamp, next_data)


@login_required
def mine(request):

    last_block = request.session['blockchain'][-1]


