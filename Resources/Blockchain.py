import hashlib
import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculates the hash of the block.

        Returns:
            str: The hash of the block.
        """
        hash_str = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(hash_str.encode('utf-8')).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.genesis_block = self.create_genesis_block()
        self.add_block(self.genesis_block)

    def create_genesis_block(self):
        """
        Creates the genesis block of the blockchain.

        Returns:
            Block: The genesis block.
        """
        return Block(0, datetime.datetime.now(), "Genesis block", "")

    def add_block(self, block):
        """
        Adds a block to the blockchain.

        Args:
            block: The block to add.
        """
        block.previous_hash = self.chain[-1].hash
        self.chain.append(block)

    def get_block(self, index):
        """
        Gets a block from the blockchain by index.

        Args:
            index: The index of the block to get.

        Returns:
            Block: The block at the given index.
        """
        if index < len(self.chain):
            return self.chain[index]
        else:
            return None

    def is_valid_chain(self):
        """
        Checks if the blockchain is valid.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True


# Create a blockchain
blockchain = Blockchain()

# Add some blocks to the blockchain
for i in range(10):
    block = Block(i, datetime.datetime.now(), "Block {} data".format(i), blockchain.chain[-1].hash)
    blockchain.add_block(block)

# Check if the blockchain is valid
if blockchain.is_valid_chain():
    print("The blockchain is valid.")
else:
    print("The blockchain is invalid.")
