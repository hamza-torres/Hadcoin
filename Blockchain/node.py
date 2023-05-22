from flask import Flask, jsonify, request
from Blockchain import Blockchain
from Transaction import Transaction

app = Flask(__name__)

blockchain = Blockchain()
nodes = []



@app.route('/join', methods=['POST'])
def join():
    """
    Add a new node to the list of nodes.
    """

@app.route('/leave', methods=['POST'])
def leave():
    """
    Remove a node from the list of nodes.
    """

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    """
    Returns the blockchain.
    """
    return jsonify(blockchain.get_chain()), 200

@app.route('/blockchain/length', methods=['GET'])
def get_blockchain_length():
    """
    Returns the length of the blockchain.
    """
    return jsonify(len(blockchain.get_chain())), 200

@app.route('/blockchain/last_block', methods=['GET'])
def get_last_block():
    """
    Returns the last block in the blockchain.
    """
    return jsonify(blockchain.get_tail()), 200

@app.route('/blockchain/block/<int:index>', methods=['GET'])
def get_block(index):
    """
    Returns the block at the given index.
    """
    block = blockchain.get_block(index)
    if block:
        return jsonify(block), 200
    return jsonify('Block not found'), 404

@app.route('/blockchain/transaction', methods=['GET'])
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
    transaction = request.get_json()
    if transaction:
        new_transaction = Transaction(
            transaction['sender'],
            transaction['receiver'],
            transaction['amount'],
            transaction['timestamp'],
            transaction['signature'],
            transaction['hash']
        )
        if blockchain.add_transaction(new_transaction):
            return jsonify('Transaction successfully added'), 201
    return jsonify('Invalid transaction'), 404

@app.route('/blockchain/mine/<public_key>', methods=['POST'])
def mine(public_key):
    """
    Mine a new block.
    """
    data = request.get_json()
    if data:
        message, block = blockchain.mine(data['key'])
        if message == 'Block Successfully Added':
            return jsonify(message, block), 201
    return jsonify('Block not mined'), 404

@app.route('/blockchain/chain/valid', methods=['GET'])
def is_valid():
    """
    Check if the blockchain is valid.
    """
    if blockchain.is_valid():
        return jsonify('Blockchain is valid'), 200
    return jsonify('Blockchain is invalid'), 404