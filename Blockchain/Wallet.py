from Transaction import Transaction
import datetime
import rsa

class Wallet:
    def __init__(self, private_key, public_key):
        """
        Returns a new Wallet object.

        Args:
            private_key (str)
            public_key (str)
        """
        self.private_key = private_key or None
        self.public_key = public_key or None
        self.balance = 0.00
        self.transactions = []

    def create_transaction(self, receiver, amount, timestamp):
        """
        Creates a transaction dictionary.

        Args:
            receiver (str)
            amount (float)
            timestamp (int)
        """
        transaction = Transaction(
            self.public_key, 
            receiver, 
            amount, 
            timestamp= str(datetime.datetime.now()),
            hash= self.hash(),
            signature= transaction.sign(self.private_key))
        return transaction

    def __repr__(self):
        return "Wallet<Public Key: {}, Balance: {}>".format(
            self.private_key,
            self.balance
        )

    # ACCESSORS ----------------------------------------------------------------
    def get_private_key(self):
        """
        Returns the private key.
        """
        return self.private_key

    def get_public_key(self):
        """
        Returns the public key.
        """
        return self.public_key
    
    def get_balance(self):
        """
        Returns the balance.
        """
        return self.balance
    
    def get_transactions(self):
        """
        Returns the transactions.
        """
        return self.transactions
    # MODIFIERS ----------------------------------------------------------------
    def set_keys(self, private_key, public_key):
        """
        Sets the keys.

        Args:
            private_key (str)
            public_key (str)
        """
        self.private_key = private_key
        self.public_key = public_key

    def set_balance(self, balance):
        """
        Sets the balance.

        Args:
            balance (float)
        """
        self.balance = balance

    def set_transactions(self, transactions):
        """
        Sets the transactions.

        Args:
            transactions (list)
        """
        self.transactions = transactions

    # METHODS ------------------------------------------------------------------
    # def send()
