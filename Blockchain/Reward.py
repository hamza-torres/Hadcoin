import hashlib

class CoinbaseTransaction:
    def __init__(self, recipient_address, amount):
        self.receiver = recipient_address
        self.amount = amount
        self.hash = self.hash_reward()


    def hash_reward(self):
        """
        Returns a hash of the transaction taking into account its attributes
        """
        key = hashlib.sha256()
        key.update(
            str(self.receiver).encode() +
            str(self.amount).encode()
        )
        return key.digest()

    def validate(self):
        """
        Returns True if the transaction is valid, False otherwise.
        """
        if self.hash != self.hash_reward():
            return False
        return True
    
    def __str__(self):
        return f"""
        >    Receiver: {self.receiver}
        >    Amount: {self.amount}
        >    Hash: {self.hash}
        """
    
    def get_amount(self):
        return self.amount
    
    
