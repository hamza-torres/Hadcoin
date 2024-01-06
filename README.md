# Project-720

## Plan of Action
- first
- second
- third


## Architecture
Software architecture of the cryptocurrency and the interactions between its components. Below is a breakdown of classes and their properties.

### **Block** - A block object used to make up the Blockchain. 
##### *Attributes*
- `index` - *Integer* - The index of the block.
- `timestamp` - *Integer* - The timestamp of the block at creation.
- `previous_hash` - *String* - The hash of the previous block in the chain.
- `transaction` - *Dict* - The transaction contained in the block.
- `difficulty` - *Integer* - The hash difficulty used to mine the block.
- `nonce` - *Integer* - The proof of work.
- `hash` - *String* - The hash of the block.

##### *Methods*
###### *Constructor*
```python
def __init__(self, index, timestamp, data, previous_hash):
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
```
###### *Instance Operations*
```python
def hash(self):
        """
        Returns a hash of the block taking into account its attributes
        """
```


### **Blockchain** - A Blockchain object made of Blocks.
##### *Attributes*
- `chain` - *list* - A list of Blocks.
- `difficulty` - *Integer* - The current hashing complexity set for mining new blocks.
- `pending_transactions` - *list* - A list of pending transactions.

##### *Methods*
###### *Constructor*
```python
def __init__(self):
        """
        Returns a new Blockchain object with a chain containing the genesis block and 
        sets the difficulty to 1.
        """
```
###### *Mutators*
```python
def add_block(self, block):
        """
        Adds a new block to the chain.

        Args:
            block (Block)
        """
``` 
```python
def add_transaction(self, transaction):
        """
        Adds a new transaction to the list of pending transactions.

        Args:
            transaction (Transaction)
        """
```

```python
def set_difficulty(self, difficulty):
        """
        Sets the difficulty of mining a new block.

        Args:
            difficulty (int)
        """
```
```python
def replace_chain(self, new_chain):
        """
        Replaces the current chain with a new chain.

        Args:
            new_chain (list)
        """
```
###### *Accessors*
```python
def get_tail(self):
        """
        Returns the latest block in the chain.
        """
```
```python
def get_block(self, index):
        """
        Returns the block at the given index.

        Args:
            index (int)
        """
```
```python
def get_difficulty(self):
        """
        Returns the current difficulty.
        """
```
```python
def get_chain(self):
        """
        Returns the chain.
        """
```
```python
def get_transactions(self):
        """
        Returns the list of pending transactions.
        """
```
###### *Instance Operations*
```python
def mine(self, miner_address):
        """
        Mines a new block with the pending transactions and adds it to the chain.

        Args:
            miner_address (str)
        """
```
```python
def validate(self):
        """
        Returns True if the chain is valid, False otherwise.
        """
```
```python
def validate_block(self, block):
        """
        Returns True if the block is valid, False otherwise.

        Args:
            block (Block)
        """
```
```python
def validate_transaction(self, transaction):
        """
        Returns True if the transaction is valid, False otherwise.

        Args:
            transaction (Transaction)
        """
```
```python
def resolve_conflicts(self):
        """
        Resolves conflicts between chains by replacing the current chain with the
        longest valid chain in the network.
        """
```


### **Transaction** - A Transaction object to be added in Blocks.
##### *Attributes*
- `sender` - *String* - The address of the sender of the transaction.
- `receiver` - *String* - The address of the receiver of the transaction
- `amount` - *Float* - The amount of the transaction.
- `timestamp` - *Integer* - The timestamp of the transaction at creation.
- `signature` - *String* - The signature of the transaction.
- `hash` - *String* - The hash of the transaction. 
##### *Methods*
###### *Constructor*
```python
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
```
###### *Instance Operations*
```python
def hash(self):
        """
        Returns a hash of the transaction taking into account its attributes
        """
```
```python
def sign(self, private_key):
        """
        Signs the transaction with the private key of the sender.

        Args:
            private_key (str)
        """
```
```python
def validate(self):
        """
        Returns True if the transaction is valid, False otherwise.
        """
```





### **Wallet** - A Wallet object used to participate in the Blockchain.
##### *Attributes*
- `public_key` - *string* - The public key of the wallet.
- `private_key` - *string* - The private key of the wallet.
- `balance` - *float* - The balance of the wallet.
- `transactions` - *list* - A list of transactions made by the wallet.

##### *Methods*
###### *Constructor*
```python
def __init__(self):
        """
        Returns a new Wallet object with a public and private key.
        """
```
###### *Mutators*
```python
def add_transaction(self, transaction):
        """
        Adds a new transaction to the list of transactions.

        Args:
            transaction (Transaction)
        """
```
```python
def set_balance(self, balance):
        """
        Sets the balance of the wallet.

        Args:
            balance (float)
        """
```
```python
def set_keys(self, public_key, private_key):
        """
        Sets the public and private keys of the wallet.

        Args:
            public_key (str)
            private_key (str)
        """
```
```python
def generate_keys(self):
        """
        Generates a new public and private key for the wallet.
        """
```
###### *Accessors*
```python
def get_balance(self):
        """
        Returns the balance of the wallet.
        """
```
```python
def get_public_key(self):
        """
        Returns the public key of the wallet.
        """
```
```python
def get_private_key(self):
        """
        Returns the private key of the wallet.
        """
```
```python
def get_transactions(self):
        """
        Returns the list of transactions.
        """
```
###### *Instance Operations*
```python
def validate(self):
        """
        Returns True if the wallet is valid, False otherwise.
        """
```
```python
def create_transaction(self, receiver, amount):
        """
        Creates a new transaction.

        Args:
            receiver (str)
            amount (float)
        """
```
```python
def validate_transaction(self, transaction):
        """
        Returns True if the transaction is valid, False otherwise.

        Args:
            transaction (Transaction)
        """
```
```python
def validate_balance(self):
        """
        Returns True if the balance of the wallet is valid, False otherwise.
        """
```
```python
def validate_keys(self):
        """
        Returns True if the keys of the wallet are valid, False otherwise.
        """
```
```python
def send(self, transaction):
        """
        Sends a transaction to the network.

        Args:
            transaction (Transaction)
        """
```




### **API** - An API object facilitating interaction with the Blockchain.
- [ ] Get the Blockchain.
- [ ] Mine a block.
- [ ] Add a transaction.
- [ ] Add a node.
- [ ] Resolve conflicts.
- [ ] Get the balance of a wallet.
- [ ] Get the list of transactions.
- [ ] Get the list of nodes.
- [ ] Get a particular block.
  





