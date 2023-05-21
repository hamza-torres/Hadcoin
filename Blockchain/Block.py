# A Block object used to make up the Blockchain
import hashlib

class Block:
    def __init__(self, 
                 index, 
                 timestamp, 
                 previous_hash, 
                 transaction, 
                 difficulty, 
                 nonce):
        """
        Returns a new Block object. Each block is "chained" to its previous block
        by its unique hash.

        Args:
            index (int)
            timestamp (int)
            data (str)
            previous_hash(str)

        Attrib:
            index (int)
            timestamp (int)
            transaction (dict)
            previous_hash (str)
            difficulty (int)
            nonce (int)
            hash(str)
        """
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.transaction = transaction
        self.difficulty = difficulty
        self.nonce = nonce
        self.hash = self.hash()

    def hash(self):
        """
        Returns a hash of the block taking into account its attributes
        """
        key = hashlib.sha256()
        key.update(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.transaction).encode('utf-8') +
            str(self.difficulty).encode('utf-8') +
            str(self.nonce).encode('utf-8')
        )
        return key.hexdigest()
    
    def __repr__(self):
        return "Block<Index: {}, Time: {}, Transaction{}, Prev_Hash: {}, Hash: {}>".format(
            self.index,
            self.timestamp,
            self.transaction,
            self.previous_hash,
            self.hash
        )
    
