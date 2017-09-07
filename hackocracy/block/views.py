from django.shortcuts import render

# Create your views here.
import hashlib
from datetime import datetime


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def __unicode__(self):
        print("This is block number {} with data : {} and hash {}".format(self.index,
                                                                          self.data,
                                                                          self.hash))


def calculate_hash(index, previous_hash, timestamp, data):
        return hashlib.sha256(index + previous_hash + timestamp + data).hexdigest()


def generate_next_block(data):  
    previous_block = get_lastest_block()
    next_index = previous_block.index + 1
    next_timestamp = datetime.now()
    next_hash = calculate_hash(next_index, previous_block.hash, next_timestamp, data)
    return Block(next_index, previous_block.hash, next_timestamp, data, next_hash)


def get_genesis_block():
    return Block(0, '0', '2017-09-02 23:41:45.944072', 'Genesis block', '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7')

def calculate_hash_for_block(new_block):
    return calculate_hash(new_block.index,
                          new_block.previous_hash,
                          new_block.timestamp,
                          new_block.data)
# ???????
blockchain = [get_genesis_block()]

# validate if a block or chain of blocks is valid
# especially when we receive new blocks from other nodes
# we must check those to decide whether to accept them or not
def is_valid_block(new_block, previous_block):
    if previous_block.index + 1 != new_block.index
        print('Invalid Index')
        return False
    elif previous_block.hash != new_block.previous_hash:
        print('Invalid previoushash')
        return False
    elif calculate_hash_for_block(new_block) != new_block.hash:
        print('Invalid hash, expected : {}, got : {}'.format(calculate_hash_for_block(new_block),
                                                             new_block.hash))
