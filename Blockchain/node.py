from flask import Flask, jsonify, request
from Blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()





@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    """
    Returns the blockchain.
    """
    return jsonify(blockchain.get_chain()), 200