# Import the ecdsa module.
# Create a new key pair.
# Store the public key in the Cryptocurrency class.
# When sending cryptocurrency, sign the transaction with the private key.
# When receiving cryptocurrency, verify the signature with the public key.
# Here is an example of how to add digital signatures to the cryptocurrency:

import blockchain
import ecdsa


class Cryptocurrency(object):
    def __init__(self, name, symbol, total_supply, decimals):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.decimals = decimals

        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256K1)
        self.public_key = self.private_key.get_verifying_key()

    def get_balance(self, address):
        return blockchain.get_balance(address, self.symbol)

    def send(self, from_address, to_address, amount):
        signature = self.private_key.sign(bytes(str(amount).encode('utf-8')))
        blockchain.send(from_address, to_address, amount, self.symbol, signature)

    def verify_signature(self, from_address, to_address, amount, signature):
        public_key = blockchain.get_public_key(from_address)
        return public_key.verify(bytes(str(amount).encode('utf-8')), signature)


my_cryptocurrency = Cryptocurrency("My Cryptocurrency", "MC", 1000000, 10)

# Mine a block
blockchain.mine_block()

# Check the balance of my account
my_balance = my_cryptocurrency.get_balance("my_address")

# Send some cryptocurrency to another account
my_cryptocurrency.send("my_address", "another_address", 100)

# Check the balance of the other account
another_balance = my_cryptocurrency.get_balance("another_address")

# Verify the signature
if my_cryptocurrency.verify_signature("my_address", "another_address", 100, signature):
    print("The signature is valid.")
else:
    print("The signature is invalid.")
