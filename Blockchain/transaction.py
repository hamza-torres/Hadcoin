




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







        """
        Sign transaction with private key
        """
        # private_key = RSA.importKey(binascii.unhexlify(self.sender))
        # signer = PKCS1_v1_5.new(private_key)
        # h = SHA.new(str(self.to_dict()).encode('utf8'))
        # self.signature = binascii.hexlify(signer.sign(h)).decode('ascii')
        # return self.signature
        