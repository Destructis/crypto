import time
import hashlib
import json

# The class Block was incorrectly defined, it should be defined as follows:
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    
    

# This function is used to create the genesis block
    def create_genesis_block():
        return Block(0, "0", time.time(), "Genesis Block", "0")
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]
    num_of_blocks_to_add = 20

# This function is used to create new blocks
    def create_new_block(previous_block, data):
        index = previous_block.index + 1
        timestamp = time.time()
        hash = calculate_hash(index, previous_block.hash, timestamp, data)
        return Block(index, previous_block.hash, timestamp, data, hash)

# This function is used to calculate the hash for a block
    def calculate_hash(index, previous_hash, timestamp, data):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')
                          
    # Create blockchain and add genesis block
   
    

    # How many blocks should we add to the chain after the genesis block
    

def write_block_to_file(block):
    filename = 'block-{}.txt'.format(block.index)
    with open(filename, 'w') as file:
        file.write("Index: {}\n".format(block.index))
        file.write("Previous Hash: {}\n".format(block.previous_hash))
        file.write("Timestamp: {}\n".format(block.timestamp))
        file.write("Data: {}\n".format(block.data))
        file.write("Hash: {}\n".format(block.hash))

def is_valid_chain(blockchain):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        # Check that the current block has a valid hash
        if current_block.hash != current_block.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
            return False

        # Check that the first block has a previous hash of 0
        if i == 1 and current_block.previous_hash != '0':
            return False

        # Check that each block's previous hash matches the hash of the previous block
        if current_block.previous_hash != previous_block.hash:
            return False

    return True


# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
    new_block_data = "Block #{} has been added to the blockchain!".format(i)
    new_block = create_new_block(previous_block, new_block_data)
    blockchain.append(new_block)
    previous_block = new_block
    print("Is the blockchain valid?", is_valid_chain(blockchain))
    print("Block #{} has been added to the blockchain!".format(new_block.index))
    print("Hash: {}\n".format(new_block.hash))
    write_block_to_file(new_block)
