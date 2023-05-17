# Blockchain
import datetime
import hashlib
import json
import random

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.datetime.now()
        self.public_key = None
    
    def __str__(self):
        return f"{self.sender} -> {self.receiver} : {self.amount} @ {self.timestamp}"


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
        hash_str = str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.difficulty) + str(self.nonce) 
        return hashlib.sha256(hash_str.encode('utf-8')).hexdigest()



class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 1
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(index = 0, 
                     timestamp= datetime.datetime.now(), 
                     transactions= "Genesis block", 
                     previous_hash= "", 
                     nonce= 1)
    
    def add_block(self, block):
        block.previous_hash = self.chain[-1].hash
        block.difficulty = self.difficulty
        self.chain.append(block)
        return block

    def get_block(self, index):
        if index < len(self.chain):
            return self.chain[index]
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
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            if current_block.hash[:current_block.difficulty] != "0" * current_block.difficulty:
                return False
            if current_block.difficulty < previous_block.difficulty:
                return False
        return True
    
    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_block(self):              
        block = Block(index = len(self.chain), 
                      timestamp = datetime.datetime.now(), 
                      previous_hash = self.chain[-1].hash,
                      transactions= '',  
                      difficulty = self.difficulty, 
                      nonce = 0)
        if self.pending_transactions[0]:
            block.transactions = self.pending_transactions[0].__str__()
        block.nonce = self.proof_of_work(block)

        if self.pending_transactions[0]:
            self.pending_transactions.pop(0)

        self.add_block(block)

        return block










