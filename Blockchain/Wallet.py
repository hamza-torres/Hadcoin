from Transaction import Transaction
import datetime
import ecdsa

class Wallet:
    def __init__(self, private_key=None, public_key=None):
        """
        Returns a new Wallet object.

        Args:
            private_key (str)
            public_key (str)
        """
        self.private_key = private_key
        self.public_key = public_key
        self.balance = 0.00
        self.transactions = []

    def create_transaction(self, receiver, amount):
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
            timestamp= str(datetime.datetime.now()))
        signature= transaction.sign(self.private_key)
        return transaction
    
    def generate_keys(self):
        """
        Generates a private key and a public key.
        """
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()


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

    def calculate_balance(self, balance):
        """
        Sets the balance.

        Args:
            balance (float)
        """
        # self.balance = balance

    def set_transactions(self, transactions):
        """
        Sets the transactions.

        Args:
            transactions (list)
        """
        # self.transactions = transactions

    # METHODS ------------------------------------------------------------------
    # def send()
