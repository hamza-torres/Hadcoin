import hashlib
import json

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
    
    def get_amount(self):
        return self.amount
    
    def __str__(self):
        return f"""
        >    Receiver: {self.receiver.to_string().hex()}
        >    Amount: {self.amount}
        >    Hash: {self.hash.hex()}
        """
    
    # def __repr__(self):
    #     rec = self.receiver.to_string().hex()
    #     rec = {'miner': rec}
    #     json_data = json.dumps(rec, default=lambda x: x.decode() if isinstance(x, bytes) else str(x))
    #     return {
    #         "receiver": str(self.receiver.to_string().hex()),
    #         "amount": self.amount,
    #         "hash": self.hash
    #     }
    
    def __repr__(self):
        return {
            "receiver": self.receiver.to_string().hex(),
            "amount": self.amount,
            "hash": self.hash.hex()
        }
