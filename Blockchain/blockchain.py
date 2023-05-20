# Blockchain
import datetime
import hashlib
import json
import random
import transaction

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, difficulty, nonce):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_str = (
            str(self.index) + 
            str(self.timestamp) + 
            str(self.transactions) + 
            str(self.previous_hash) + 
            str(self.nonce) + 
            str(self.difficulty))  
        return hashlib.sha256(hash_str.encode()).hexdigest()



class Blockchain:
    def __init__(self):
        self.difficulty = 1
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(index = 1, 
                     timestamp= str(datetime.datetime.now()), 
                     transactions= "Genesis block", 
                     previous_hash= None,
                     difficulty= 1,
                     nonce= 1)
    
    def add_block(self, block):
        if block.previous_hash != self.get_latest_block().hash:
            return False
        if block.difficulty != self.difficulty:
            return False
        self.chain.append(block)
        return block.__dict__

    def get_block(self, index):
        if index < len(self.chain) + 1 and index > 0:
            return self.chain[index-1].__dict__
        return None
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, block):
        valid_proof = False
        while not valid_proof:
            nonce = random.randint(0, 2**32)
            block.nonce = nonce
            hash = block.calculate_hash()
            if hash[:self.difficulty] == "0" * self.difficulty:
                valid_proof = True
        return nonce
    
    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                print(f"Current hash is invalid of block {current_block.index}")
                return False
            if current_block.previous_hash != previous_block.hash:
                print(f"Previous hash is invalid of block {current_block.index}")
                return False
            if current_block.hash[:current_block.difficulty] != "0" * current_block.difficulty:
                print(f"Block {current_block.index} has a mismatched difficulty")
                return False
            if current_block.difficulty < previous_block.difficulty:
                print(f"Block {current_block.index} has a lower difficulty than previous block")
                return False
        return True
    
    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_block(self):              
        block = Block(index = len(self.chain) + 1, 
                      timestamp = str(datetime.datetime.now()),
                      previous_hash = self.get_latest_block().hash,
                      transactions= None,  
                      nonce = 0,
                      difficulty = self.difficulty) 
        if self.pending_transactions:
            # block.transactions = self.pending_transactions[0]
            block.transactions = self.pending_transactions[0].__dict__
            block.nonce = self.proof_of_work(block)
            block.hash = block.calculate_hash()
            self.pending_transactions.pop(0)
        else:
            block.nonce = self.proof_of_work(block)
            block.hash = block.calculate_hash()

        return self.add_block(block)
        
    

    def get_chain(self):
        if self.chain:
            ret_chain = []
            for block in self.chain:
                ret_chain.append(block.__dict__)
            return ret_chain
        return None
  
  



blockchain = Blockchain()
transaction1 = transaction.Transaction("Jack", "Man", 100)
transaction2 = transaction.Transaction("John", "Noman", 500)
transaction3 = transaction.Transaction("Jim", "Yesman", 700)
transaction4 = transaction.Transaction("Man", "Yesman", 10)
transaction5 = transaction.Transaction("Man", "Yesman", 20)
transaction6 = transaction.Transaction("Jim", "Man", 20)

blockchain.add_transaction(transaction1)
blockchain.add_transaction(transaction2)
blockchain.add_transaction(transaction3)
blockchain.add_transaction(transaction4)
blockchain.add_transaction(transaction5)
blockchain.add_transaction(transaction6)


print(blockchain.mine_block())
print('\n')
print(blockchain.mine_block())
print('\n')
print(blockchain.mine_block())
print('\n')
print(blockchain.mine_block())
print('\n')
print(blockchain.mine_block())
print('\n')
print(blockchain.get_chain())
print('\n')

print(blockchain.validate_blockchain())


# print('\n')
# print(blockchain.get_block(2)['transactions']['sender'])