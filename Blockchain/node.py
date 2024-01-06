from flask import Flask, jsonify, request
from Blockchain import Blockchain
from Transaction import Transaction
from Wallet import Wallet
import ecdsa
import requests
from uuid import uuid4
from urllib.parse import urlparse

app = Flask(__name__)

blockchain = Blockchain()
wallet = Wallet()
wallet.generate_keys()


@app.route('/join', methods=['POST']) #WORKING - ADD THIS NODE
def join():
    """
    Add a new node to the list of nodes.
    """
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node found', 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': 'Node added',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201



@app.route('/blockchain', methods=['GET']) #WORKING
def get_blockchain():
    """
    Returns the blockchain.
    """
    # chain = []
    # for block in blockchain.chain:
    #     chain.append(block.__repr__())
    response = {
        'chain': blockchain.get_chain(),
        'length': len(blockchain.get_chain())
    }
    return jsonify(response), 200


@app.route('/blockchain/length', methods=['GET']) #WORKING
def get_blockchain_length():
    """
    Returns the length of the blockchain.
    """
    return jsonify(len(blockchain.get_chain())), 200


@app.route('/leave', methods=['POST']) #WORKING
def leave():
    """
    Remove a node from the list of nodes.
    """
    json = request.get_json()
    node = json.get('node')
    if node is None:
        return 'No node found', 400
    blockchain.remove_node(node)
    response = {
        'message': 'Node removed',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/blockchain/last_block', methods=['GET']) #WORKING
def get_last_block():
    """
    Returns the last block in the blockchain.
    """
    return jsonify(blockchain.get_tail().__repr__()), 200


@app.route('/blockchain/block/<int:index>', methods=['GET']) #WORKING
def get_block(index):
    """
    Returns the block at the given index.
    """
    block = blockchain.get_block(index)
    if blockchain.get_block(index):
        return jsonify(block.__repr__()), 200
    return jsonify('Block not found'), 404


@app.route('/blockchain/transactions', methods=['GET'])
def get_pending_transactions():
    """
    Returns the pending transactions.
    """
    pending_transactions = blockchain.get_pending_transactions()
    if pending_transactions:
        return jsonify(pending_transactions), 200
    return jsonify('No pending transactions'), 404


@app.route('/blockchain/transaction', methods=['POST'])
def add_transaction():
    """
    Add a transaction to the list of pending transactions.
    """
    data = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount', 'hash', 'signature', 'timestamp']
    if not all(key in data for key in transaction_keys):
        return jsonify('Transaction data incomplete'), 400
    # public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(data['sender']), curve=ecdsa.SECP256k1)
    sender = ecdsa.VerifyingKey.from_string(bytes.fromhex(data['sender']))
    hash = bytes.fromhex(data['hash'])
    transaction = Transaction(sender, 
                              data['receiver'], 
                              data['amount'], 
                              data['timestamp'], 
                              data['signature'], 
                              hash)
    message, trans = blockchain.add_transaction(transaction)
    if message == 'Transaction Successfully Added':
        return jsonify(message), 201
    return jsonify('Transaction not added'), 400


@app.route('/blockchain/mine', methods=['GET'])
def mine():
    """
    Mine a new block.
    """
    key = wallet.get_public_key()
    
    message, block = blockchain.mine(key)
    if message == 'Block Successfully Added':
        return jsonify(message), 201
    return jsonify('Block not mined'), 404


@app.route('/blockchain/chain/valid', methods=['GET'])
def is_valid():
    """
    Check if the blockchain is valid.
    """
    if blockchain.is_valid():
        return jsonify('Blockchain is valid'), 200
    return jsonify('Blockchain is not valid'), 404


app.run(host = '0.0.0.0', port = 5000)