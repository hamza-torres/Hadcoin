import datetime
import hashlib
import ecdsa

class Transaction:
    def __init__(self, sender, receiver, amount, timestamp):
        """
        Returns a new Transaction object.

        Args:
            sender (str)
            receiver (str)
            amount (float)
            timestamp (int)
            hash (str)
            signature (str)
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp
        self.hash = self.hash_transaction()
        self.signature = None

    def hash_transaction(self):
        """
        Returns a hash of the transaction taking into account its attributes
        """
        key = hashlib.sha256()
        key.update(
            str(self.sender).encode() +
            str(self.receiver).encode() +
            str(self.amount).encode() +
            str(self.timestamp).encode()
        )
        return key.digest()
    
    def sign(self, private_key):
        """
        Signs the transaction with the private key of the sender.

        Args:
            private_key (str)
        """
        self.signature = private_key.sign_deterministic(self.hash)

    def verify(self, public_key):
        """
        Verifies the signature of the transaction with the public key of the sender.

        Args:
            public_key (str)
        """

        return public_key.verify(self.signature, self.hash)
    
    def __str__(self):
        return f"""
        >   Sender: {self.sender}
        >   Receiver: {self.receiver}
        >   Amount: {self.amount}
        >   Timestamp: {self.timestamp}
        >   Hash: {self.hash}
        >   Signature: {self.signature}
        """


