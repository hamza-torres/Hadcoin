




class Transaction:
    """
    A transaction which can be added to a block in the chain.
    """

    def __init__(self, sender, recipient, amount):
        """
        Constructor for the `Transaction` class.
        :param sender: The sender of the coins.
        :param recipient: The recipient of the coins.
        :param amount: The amount of coins sent.
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None

    def __repr__(self):
        return str(self.__dict__)