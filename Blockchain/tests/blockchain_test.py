import sys
sys.path.append("..")
from Blockchain import Blockchain
from Block import Block 
from Transaction import Transaction
import datetime
from ecdsa import SigningKey, NIST384p



# TESTS ----------------------------------------------------------------
def test_blockchain():
    # Initialize
    blockchain = Blockchain()
    assert len(blockchain.chain) == 1, 'Wrong number of blocks'
    assert blockchain.difficulty == 1, 'Wrong difficulty'
    assert blockchain.pending_transactions == [], 'Wrong pending transactions'
    # Genesis Block
    assert blockchain.chain[0].index == 1, 'Wrong index of genesis block'
    assert blockchain.chain[0].previous_hash == None, 'Wrong previous hash of genesis block'
    assert blockchain.chain[0].transaction == {"Genesis Block": 0}, 'Wrong transaction of genesis block'
    assert blockchain.chain[0].difficulty == 1, 'Wrong difficulty of genesis block'
    assert blockchain.chain[0].nonce == 0, 'Wrong nonce of genesis block'

def test_add_block():
    blockchain = Blockchain()
    # Index taken
    block = Block(
        index=1,
        timestamp=str(datetime.datetime.now()),
        previous_hash=blockchain.chain[-1].hash,
        transaction=None,
        difficulty=blockchain.difficulty,
        nonce=0
    )
    assert blockchain.add_block(block) == False, 'Block should not be added: iNCORRECT INDEX'
    
    # Index out of bounds
    block = Block(
        index=5,
        timestamp=str(datetime.datetime.now()),
        previous_hash=blockchain.chain[-1].hash,
        transaction=None,
        difficulty=blockchain.difficulty,
        nonce=0
    )
    assert blockchain.add_block(block) == False, 'Block should not be added: INCORRECT INDEX'
    
    # Previous hash incorrect
    block = Block(
        index=blockchain.chain[-1].index + 1,
        timestamp=0,
        previous_hash='OHDOIFWIEFH9WEHF',
        transaction=None,
        difficulty=1,
        nonce=0
    )
    assert blockchain.add_block(block) == False, 'Block should not be added: INCORRECT PREVIOUS HASH'

    # Incorrect difficulty
    block = Block(
        index=blockchain.chain[-1].index + 1,
        timestamp=0,
        previous_hash=blockchain.chain[-1].hash,
        transaction=None,
        difficulty=2,
        nonce=0
    )
    block.hash = 'HDOIFWIEFH9WEHF'
    assert blockchain.add_block(block) == False, 'Block should not be added: INCORRECT DIFFICULTY'
    
    # Incorrect chain length
    assert len(blockchain.chain) == 1, 'Wrong number of blocks'

    # Correct block
    block = Block(
        index=blockchain.chain[-1].index + 1,
        timestamp=str(datetime.datetime.now()),
        previous_hash=blockchain.chain[-1].hash,
        transaction=None,
        difficulty=blockchain.difficulty,
        nonce=0
    )
    block.hash = '0' * blockchain.difficulty + 'HDOIFWIEFH9WEHF'
    assert blockchain.add_block(block) == ('Block Successfully Added', block), 'Block should be added'
    assert len(blockchain.chain) == 2, 'Wrong number of blocks'


def test_add_transaction():
    blockchain = Blockchain()
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    sk1 = SigningKey.generate() # uses NIST192p
    vk1 = sk1.verifying_key


    transaction = Transaction(
        sender=vk,
        receiver="John",
        amount=10,
        timestamp=str(datetime.datetime.now())
    )
    transaction.signature = sk.sign(transaction.hash)
    # print(transaction.__dict__)

    # Block should be added
    assert blockchain.add_transaction(transaction) == ('Transaction Successfully Added', transaction)
    assert len(blockchain.pending_transactions) == 1, 'Wrong number of pending transactions'

    # Transaction already in pending transactions 
    assert blockchain.add_transaction(transaction) == False, 'Transaction already in pending transactions'

    # Transaction invalid
    transaction2 = Transaction(
        sender=vk1,
        receiver="John",
        amount=10,
        timestamp=str(datetime.datetime.now())
    )
    transaction2.signature = sk.sign(transaction2.hash)
    try:
        blockchain.add_transaction(transaction2)
        print('Transaction should not be added')
    except Exception as e:
        pass
    
    # Transaction valid
    transaction2.signature = sk1.sign(transaction2.hash)
    assert blockchain.add_transaction(transaction2) == ('Transaction Successfully Added', transaction2)
    assert len(blockchain.pending_transactions) == 2, 'Wrong number of pending transactions'


def test_mine_block():
    blockchain = Blockchain()
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    sk1 = SigningKey.generate() # uses NIST192p
    vk1 = sk1.verifying_key

    transaction = Transaction(
        sender=vk,
        receiver="John",
        amount=10,
        timestamp=str(datetime.datetime.now())
    )
    transaction.signature = sk.sign(transaction.hash)
    blockchain.add_transaction(transaction)

    transaction2 = Transaction(
        sender=vk1,
        receiver="John",
        amount=10,
        timestamp=str(datetime.datetime.now())
    )
    transaction2.signature = sk1.sign(transaction2.hash)
    blockchain.add_transaction(transaction2)

    blockchain.mine()
    blockchain.mine()
    blockchain.mine()

    assert len(blockchain.chain) == 4, 'Wrong number of blocks'
    # for block in blockchain.chain:
    #     print(block.__str__())
    #     # print(block.transaction.__str__())
    #     print('\n')



def test_set_difficulty():
    blockchain = Blockchain()
    assert blockchain.difficulty == 1, 'Wrong difficulty of genesis block'
    for i in range(1, 5000):
        blockchain.mine()
    assert blockchain.difficulty == 3, 'Wrong difficulty'
    for block in blockchain.chain:
        print(f'Block {block.index}, difficulty: {block.difficulty}')



def test_get_tail():
    blockchain = Blockchain()
    assert blockchain.get_tail() == blockchain.chain[-1]

def test_get_block():
    blockchain = Blockchain()
    for i in range(1, 5):
        blockchain.mine()

    assert blockchain.get_block(1) == blockchain.chain[0], 'Wrong block'
    assert blockchain.get_block(3) == blockchain.chain[2], 'Wrong block'
    assert blockchain.get_block(8) == None, 'Block does not exist'


def test_get_chain():
    blockchain = Blockchain()
    for i in range(1, 5):
        blockchain.mine()
    assert blockchain.get_chain() == blockchain.chain

def test_get_pending_transactions():
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    blockchain = Blockchain()
    assert blockchain.get_pending_transactions() == None
    transaction = Transaction(
        sender=vk,
        receiver="1",
        amount=1,
        timestamp=str(datetime.datetime.now())
    )
    transaction.signature = sk.sign(transaction.hash)
    blockchain.add_transaction(transaction)
    assert blockchain.get_pending_transactions() == [transaction]

def test_proof_of_work():
    blockchain = Blockchain()
    for i in range(1, 5000):
        blockchain.mine()
    assert blockchain.get_block(5).hash.startswith('0' * 1), 'Wrong difficulty'
    assert blockchain.get_block(2020).hash.startswith('0' * 2), 'Wrong difficulty'
    assert blockchain.get_block(4500).hash.startswith('0' * 3), 'Wrong difficulty'

def test_validate():
    blockchain = Blockchain()
    for i in range(1, 100):
        blockchain.mine()

    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key

    transaction = Transaction(
        sender=vk,
        receiver="John",
        amount=10,
        timestamp=str(datetime.datetime.now())
    )
    transaction.signature = sk.sign(transaction.hash)
    blockchain.add_transaction(transaction)
    blockchain.mine()

    assert blockchain.validate() == True, 'Blockchain should be valid'
    

# def test_is_valid():
#     blockchain = Blockchain()
#     assert blockchain.is_valid() == True
#     blockchain.chain.append(Block(
#         index=2,
#         timestamp=0,
#         previous_hash=blockchain.chain[-1].hash,
#         transaction={"Genesis Block": 0},
#         difficulty=1,
#         nonce=0
#     ))
#     assert blockchain.is_valid() == False
#     blockchain.chain.append(Block(
#         index=3,
#         timestamp=0,
#         previous_hash=blockchain.chain[-1].hash,
#         transaction={"Genesis Block": 0},
#         difficulty=1,
#         nonce=0
#     ))
#     assert blockchain.is_valid() == False
#     blockchain.chain.append(Block(
#         index=4,
#         timestamp=0,
#         previous_hash=blockchain.chain[-1].hash,
#         transaction={"Genesis Block": 0},
#         difficulty=2,
#         nonce=0
#     ))
#     assert blockchain.is_valid() == False
#     blockchain.chain.append(Block(
#         index=5,
#         timestamp=0,
#         previous_hash=blockchain.chain[-1].hash,
#         transaction={"Genesis Block": 0},
#         difficulty=2,
#         nonce=0
#     ))
#     assert blockchain.is_valid() == False
#     blockchain.chain.append(Block(
#         index=6,
#         timestamp=0,
#         previous_hash=blockchain.chain[-1].hash,
#         transaction={"Genesis Block": 0},
#         difficulty=2,
#         nonce=0
#     ))
#     assert blockchain.is_valid() == False
#     blockchain.chain.append(Block(
#         index=7,
#         timestamp=0,
#         previous_hash=blockchain.chain[-1].hash,
#         transaction={"Genesis Block": 0},
#         difficulty=2,
#         nonce=0
#     ))
#     assert blockchain.is_valid() == False
#     blockchain.chain.append(Block(
#         index=8,
#         timestamp=0,
#         previous_hash=blockchain.chain[-1].hash,
#         transaction={"Genesis Block": 0},
#         difficulty=2,
#         nonce=0
#     ))
#     assert blockchain.is_valid() == False
#     blockchain.chain.append(Block(
#         index=9,
#         timestamp=0,
#         previous_hash=blockchain.chain[-1].hash,
#         transaction={"Genesis Block": 0},
#         difficulty=2,
#         nonce=0
#     ))
#     assert blockchain.is_valid() == False
#     blockchain.chain.append(Block(
#         index=10,
#         timestamp=0,
#         previous_hash=blockchain.chain[-1].hash,
#         transaction={"Genesis Block": 0},
#         difficulty=2,
#         nonce=0
#     ))
#     assert blockchain.is_valid() == False



test_blockchain()
test_add_block()
test_add_transaction()
test_mine_block()
# test_set_difficulty()
test_get_tail()
test_get_block()
test_get_chain()
test_get_pending_transactions()
# test_proof_of_work()
test_validate()
# test_is_valid()