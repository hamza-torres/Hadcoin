import datetime
import hashlib
import rsa

class Transaction:
    def __init__(self, sender, receiver, amount, timestamp, hash, signature):
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
        self.hash = self.hash()
        self.signature = signature

    def hash(self):
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
        return key.hexdigest()
    
    def sign(self, private_key):
        """
        Signs the transaction with the private key of the sender.

        Args:
            private_key (str)
        """
        self.signature = rsa.sign(self.hash.encode(), private_key, 'SHA-256')

    def verify(self, public_key):
        """
        Verifies the signature of the transaction with the public key of the sender.

        Args:
            public_key (str)
        """
        return rsa.verify(self.hash.encode(), self.signature, public_key)

    def __repr__(self):
        return "Transaction<From: {}, To: {}, Amount: {}, Time: {}, Hash: {}>".format(
            self.sender,
            self.receiver,
            self.amount,
            self.timestamp,
            self.hash
        )
