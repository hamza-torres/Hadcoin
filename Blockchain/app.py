import Blockchain
from flask import Flask, jsonify

app = Flask(__name__)

# Blockchain
blockchain = Blockchain()

# Mining
@app.route('/mineBlock', methods = ['GET'])
def mineBlock():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    proof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    block = blockchain.createBlock(proof, previousHash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previousHash': block['previousHash']}
    return jsonify(response), 200

# Getting Blockchain
@app.route('/getChain', methods = ['GET'])
def getChain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking Blockchain validity
@app.route('/isChainValid', methods = ['GET'])
def isChainValid():
    isChainValid = blockchain.isChainValid(blockchain.chain)
    if isChainValid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is invalid.'}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000)