import Block
import random
import datetime

class Blockchain:
    def __init__(self):
        """
        Returns a new Blockchain object with a chain containing the genesis block and 
        sets the difficulty to 1.
        """
        self.chain = [Block.Block(
            index=1,
            timestamp=0,
            previous_hash=None,
            transaction={"Genesis Block": 0},
            difficulty=1,
            nonce=0
        )]
        self.difficulty = 1
        self.pending_transactions = []

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
            return 'Block Successfully Added', block
        return False

    def add_transaction(self, transaction):
            """
            Adds a new transaction to the list of pending transactions.

            Args:
                transaction (Transaction)
            """
            if transaction.is_valid() and \
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
        self.difficulty = int(self.chain[-1].index/2016)


    def replace_chain(self, new_chain):
        """
        Replaces the current chain with a new chain.

        Args:
            new_chain (list)
        """
        if len(new_chain) > len(self.chain):
            self.chain = new_chain
            return 'Chain Successfully Replaced', self.chain
        return False
    
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
        return self.chain
    
    def get_pending_transactions(self):
        """
        Returns the list of pending transactions.
        """
        if self.pending_transactions:
            return self.pending_transactions
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
            hash = block.hash()
            if hash[:self.difficulty] == "0" * self.difficulty:
                valid_proof = True
        return nonce


    def mine(self):
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
        if self.pending_transactions:
            block.transaction = self.pending_transactions[0]
            block.nonce = self.proof_of_work(block)
            block.hash = block.hash()
            self.pending_transactions.pop(0)
        else:
            block.nonce = self.proof_of_work(block)
            block.hash = block.hash()
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
        return True
    
    def validate_block(self, block):
        """
        Returns True if the block is valid, False otherwise.
        """
        if block.hash != block.hash():
            return False
        if block.previous_hash != self.get_block(block.index - 1).hash:
            return False
        if block.hash[:block.difficulty] != "0" * block.difficulty:
            return False
        if block.difficulty < self.get_block(block.index - 1).difficulty:
            return False
        return True
    














    def __repr__(self):
        return "Blockchain<difficulty: {}, chain: {}>".format(
            self.difficulty,
            self.chain
        )   
        