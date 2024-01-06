from Block import Block
from Transaction import Transaction
from Reward import CoinbaseTransaction 
from urllib.parse import urlparse
import random
import datetime
import math
import requests


class Blockchain:
    def __init__(self):
        """
        Returns a new Blockchain object with a chain containing the genesis block and 
        sets the difficulty to 1.
        """
        self.chain = [Block(
            index=1,
            timestamp=str(datetime.datetime.now()),
            previous_hash=None,
            transaction={"Genesis Block": 0},
            difficulty=1,
            nonce=0
        )]   
        self.difficulty = 1
        self.reward = 50
        self.pending_transactions = []
        self.nodes = set()

    def add_block(self, block):
        """
        Adds a new block to the chain.

        Args:
            block (Block)
        """
        if block.index == self.chain[-1].index + 1 and \
            block.previous_hash == self.chain[-1].hash and \
            block.hash.startswith('0' * self.difficulty):
            self.chain.append(block)
            self.set_difficulty()
            return 'Block Successfully Added', block
        return False

    def add_transaction(self, transaction):
            """
            Adds a new transaction to the list of pending transactions.

            Args:
                transaction (Transaction)
            """
            if transaction.verify(transaction.sender) and \
                transaction not in self.pending_transactions:
                self.pending_transactions.append(transaction)
                return 'Transaction Successfully Added', transaction
            return False 


    def set_difficulty(self):
        """
        Sets the difficulty of mining a new block.

        Args:
            difficulty (int)
        """
        self.difficulty = math.ceil(self.chain[-1].index/2016)
        if self.difficulty < 1:
            self.difficulty = 1
        # return 'Difficulty Successfully Set', self.difficulty

    def set_reward(self):
        """
        Sets the reward for mining a new block.

        Args:
            reward (int)
        """
        initial_reward = 50  # Initial reward amount
        halving_interval = 200  # Number of blocks after which reward halves
        self.reward = initial_reward / (2 ** (self.chain[-1].index // halving_interval))
        return self.reward


    def replace_chain(self, network):
        """
        Replaces the chain with the longest chain in the network.

        Args:
            network (list)
        """
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_valid_chain(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
    def add_node(self, address):
        """
        Adds a new node to the network.

        Args:
            address (str)
        """
        url = urlparse(address)
        self.nodes.add(url.netloc)

    def remove_node(self, address):
        """
        Removes a node from the network.

        Args:
            address (str)
        """
        url = urlparse(address)
        self.nodes.remove(url.netloc)
        
    
    # ACCESSORS ----------------------------------------------------------------
    def get_tail(self):
        """
        Returns the latest block in the chain.
        """
        return self.chain[-1]
    
    def get_block(self, index):
        """
        Returns the block at the given index.

        Args:
            index (int)
        """
        if index < len(self.chain) + 1 and index > 0:
            return self.chain[index-1]
        return None
    
    def get_difficulty(self):
        """
        Returns the current difficulty.
        """
        return self.difficulty
    
    def get_chain(self):
        """
        Returns the chain.
        """
        chain = []
        for block in self.chain:
            chain.append(block.__repr__())
        return chain
    
    def get_pending_transactions(self):
        """
        Returns the list of pending transactions.
        """
        if self.pending_transactions:
            transactions = []
            for transaction in self.pending_transactions:
                transactions.append(transaction.__repr__())
            return transactions
        return None

# OPERATIONS ----------------------------------------------------------------
    def proof_of_work(self, block):
        """
        Calculates the proof of work of a block and returns the nonce.

        Args:
            block (Block)
        """
        valid_proof = False
        while not valid_proof:
            nonce = random.randint(0, 2**32)
            block.nonce = nonce
            hash = block.hash_block()
            if hash[:self.difficulty] == "0" * self.difficulty:
                valid_proof = True
        return nonce


    def mine(self, public_key):
        """
        Mines a new block with the pending transactions and adds it to the chain.
        """
        block = Block(
            index=self.chain[-1].index + 1,
            timestamp= str(datetime.datetime.now()),
            previous_hash=self.chain[-1].hash,
            transaction= None,
            difficulty=self.difficulty,
            nonce=0
        )
        block.reward = CoinbaseTransaction(public_key, self.set_reward())
        if self.pending_transactions:
            block.transaction = self.pending_transactions[0]
            block.nonce = self.proof_of_work(block)
            block.hash = block.hash_block()
            self.pending_transactions.pop(0)
        else:
            block.nonce = self.proof_of_work(block)
            block.hash = block.hash_block()
        return self.add_block(block)


    def validate(self):
        """
        Returns True if the chain is valid, False otherwise.
        """
        for block in self.chain:
            if block.index == 1:
                continue
            if not self.validate_block(block):
                return False
            if block.transaction:
                if not self.validate_transaction(block.transaction):
                    return False
        for transaction in self.pending_transactions:
            if not self.validate_transaction(transaction):
                return False
        return True
    
    def validate_block(self, block):
        """
        Returns True if the block is valid, False otherwise.
        """
        if block.hash != block.hash_block():
            return False
        if block.previous_hash != self.get_block(block.index - 1).hash:
            return False
        if block.hash[:block.difficulty] != "0" * block.difficulty:
            return False
        if block.difficulty < self.get_block(block.index - 1).difficulty:
            return False
        return True
    
    def validate_transaction(self, transaction):
        """
        Returns True if the transaction is valid, False otherwise.
        """
        if transaction.verify(transaction.sender):
            return True
        return False
    
    def validate_reward(self, transaction):
        """
        Returns True if the reward transaction is valid, False otherwise.
        """
        if transaction.verify(transaction.sender):
            return True
        return False
    
    def verify_key(self, public_key):
        """
        Returns True if the public key is valid, False otherwise.
        """
        # if public_key in self.wallets:
        #     return True
        # return False



    def __repr__(self):
        return "Blockchain<difficulty: {}, chain: {}>".format(
            self.difficulty,
            self.chain
        )   
        


