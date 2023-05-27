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
        self.reward = None
        self.hash = self.hash_block()

    def hash_block(self):
        """
        Returns a hash of the block taking into account its attributes
        """
        hash_str = (
                str(self.index) + 
                str(self.timestamp) + 
                str(self.transaction) + 
                str(self.previous_hash) + 
                str(self.nonce) + 
                str(self.difficulty)+
                str(self.reward))  
        return hashlib.sha256(hash_str.encode()).hexdigest()


    def __str__(self):
        return f"""
        Index: {self.index}
        Timestamp: {self.timestamp}
        Transaction: {self.transaction.__str__()}
        Previous Hash: {self.previous_hash}
        Difficulty: {self.difficulty}
        Nonce: {self.nonce}
        Reward: {self.reward}
        Hash: {self.hash}
        """
    
    def __repr__(self):
        # if self.reward == None:
        #     return {
        #         "index": self.index,
        #         "timestamp": self.timestamp,
        #         "transaction": self.transaction,
        #         "previous_hash": self.previous_hash,
        #         "difficulty": self.difficulty,
        #         "nonce": self.nonce,
        #         "hash": self.hash
        #     }
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transaction": self.transaction.__repr__(),
            "previous_hash": self.previous_hash,
            "difficulty": self.difficulty,
            "reward": self.reward.__repr__(),
            "nonce": self.nonce,
            "hash": self.hash
        }
    

    # def __repr__(self):
    #     return {
    #         "index": self.index,
    #         "timestamp": self.timestamp,
    #         "transaction": self.transaction,
    #         "previous_hash": self.previous_hash,
    #         "difficulty": self.difficulty,
    #         "nonce": self.nonce,
    #         "reward": self.reward.__repr__(),
    #         "hash": self.hash
    #     }