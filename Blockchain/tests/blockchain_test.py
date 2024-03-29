import sys
sys.path.append("..")
from Blockchain import Blockchain
from Block import Block 
from Transaction import Transaction
from Wallet import Wallet
import datetime
from ecdsa import SigningKey, NIST384p
import ecdsa



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
    # private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    # public_key = private_key.get_verifying_key()
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
    print(blockchain.get_pending_transactions())

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

    blockchain.mine(vk)
    blockchain.mine(vk)
    blockchain.mine(vk1)
    assert len(blockchain.chain) == 4, 'Wrong number of blocks'

    for i in range(1, 210):
        blockchain.mine(vk)

    for block in blockchain.chain:
        if block.index == 1:
            continue
        assert block.reward != None, f'Wrong reward amount {block.index}'
        # assert block.reward.amount == 50 / (2 ** (block.index // 200)), f'Wrong reward amount {block.index}'
        # print(f'Block {block.index}, reward: {block.reward.get_amount()}')

    # for block in blockchain.chain:
    #     print(block)
    #     # print(block.transaction.__str__())
    #     print('\n')



def test_set_difficulty():
    blockchain = Blockchain()
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    assert blockchain.difficulty == 1, 'Wrong difficulty of genesis block'
    for i in range(1, 5000):
        blockchain.mine(vk)
    assert blockchain.difficulty == 3, 'Wrong difficulty'
    for block in blockchain.chain:
        print(f'Block {block.index}, difficulty: {block.difficulty}')



def test_get_tail():
    blockchain = Blockchain()
    assert blockchain.get_tail() == blockchain.chain[-1]

def test_get_block():
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    blockchain = Blockchain()
    for i in range(1, 5):
        blockchain.mine(vk)

    assert blockchain.get_block(1) == blockchain.chain[0], 'Wrong block'
    assert blockchain.get_block(3) == blockchain.chain[2], 'Wrong block'
    assert blockchain.get_block(8) == None, 'Block does not exist'


def test_get_chain():
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    blockchain = Blockchain()
    for i in range(1, 5):
        blockchain.mine(vk)
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
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    blockchain = Blockchain()
    for i in range(1, 5000):
        blockchain.mine(vk)
    assert blockchain.get_block(5).hash.startswith('0' * 1), 'Wrong difficulty'
    assert blockchain.get_block(2020).hash.startswith('0' * 2), 'Wrong difficulty'
    assert blockchain.get_block(4500).hash.startswith('0' * 3), 'Wrong difficulty'

def test_validate():
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    blockchain = Blockchain()
    for i in range(1, 100):
        blockchain.mine(vk)

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
    blockchain.mine(vk)

    assert blockchain.validate() == True, 'Blockchain should be valid'
    

def test_wallet_creation():
    wallet = Wallet()
    assert wallet.private_key == None, 'Private key should be None'
    assert wallet.public_key == None, 'Public key should be None'

def test_wallet_new_keys():
    wallet = Wallet()
    wallet.generate_keys()
    assert wallet.private_key != None, 'Private key should not be None'
    assert wallet.public_key != None, 'Public key should not be None'

    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    wallet.set_keys(sk, vk)

    assert wallet.private_key == sk, 'Private key should be equal'
    assert wallet.public_key == vk, 'Public key should be equal'

def test_wallet_transaction():
    wallet = Wallet()
    wallet.generate_keys()

    transaction = wallet.create_transaction('John', 10)
    assert transaction.sender == wallet.public_key, 'Sender should be equal'
    assert transaction.receiver == 'John', 'Receiver should be equal'
    assert transaction.amount == 10, 'Amount should be equal'
    assert transaction.signature != None, 'Signature should not be None'
    assert transaction.verify(wallet.public_key) == True, 'Signature should be valid'


def test_keys():
    private_key = ecdsa.SigningKey.generate()
    public_key = private_key.get_verifying_key()



    st_key = public_key.to_string().hex()
    print(st_key)
    


    new_public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(st_key))
    print(new_public_key.to_string().hex())
    print(new_public_key)



    # new = ecdsa.SigningKey.from_string(bytes.fromhex(st_key), curve=ecdsa.SECP256k1)
    # newvk = ecdsa.verifying_key.from_string(bytes.fromhex(st_key), curve=ecdsa.SECP256k1)
    
def test_recover_key():
    key = "a9d42ed5770ce92f28ebad41955a0f6f67825fb784aa1aee968c590ca9a427d2fbce4e2dd03abd9d94d83a4ecac6a727"
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(key))

    hash = "2b2ba055d61da14b9e601ed49389c5a5c7652c9fe1acf365780a88e30bb16ef0"
    hash = bytes.fromhex(hash)

    sig = "d6c811cf2c29cc67575a9f847f2575eb7fa935c358a23cd06922f83068b98b1caa24cccc0741dd2ed291fc5e237ea8dc"
    sig = bytes.fromhex(sig)

    t = Transaction(
        vk,
        "John",
        10,
        "2023-05-26 22:44:37.651999",
        hash,
        sig
    )
    
    print(vk.verify(sig, hash))
    print(t.verify())


test_recover_key()
# test_keys()
# test_blockchain()
# test_add_block()
# test_add_transaction()
# test_mine_block()
# # test_set_difficulty()
# test_get_tail()
# test_get_block()
# test_get_chain()
# test_get_pending_transactions()
# # test_proof_of_work()
# test_validate()

# test_wallet_creation()
# test_wallet_new_keys()
# test_wallet_transaction()

