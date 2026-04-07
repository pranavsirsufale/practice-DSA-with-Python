import datetime, hashlib, json
from flask import Flask, jsonify

class BlockChain:
    def __init__(self):
        self.chain = []
        self.createBlock(proof=1, previousHash='0')

    def createBlock(self, proof, previousHash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previousHash": previousHash
        }
        self.chain.append(block)
        return block

    def printPreviousBlock(self):
        return self.chain[-1]

    def proofOfWork(self, previousProof):
        newProof = 1
        checkProof = False
        while checkProof is False:
            hashOperation = hashlib.sha256(
                str(newProof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:5] == '00000':
                checkProof = True
            else:
                newProof += 1
        return newProof

    def hash(self, block):
        encodeBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodeBlock).hexdigest()

    def chainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['previousHash'] != self.hash(previousBlock):
                return False
            previousProof = previousBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(
                str(proof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:5] != '00000':
                return False
            previousBlock = block
            blockIndex += 1
        return True

app = Flask(__name__)
blockchain = BlockChain()

@app.route('/mine_block', methods=['GET'])
def mineBlock():
    previousBlock = blockchain.printPreviousBlock()
    previousProof = previousBlock['proof']
    proof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    block = blockchain.createBlock(proof, previousHash)
    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previousHash']
    }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def getChain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def isValid():
    isValid = blockchain.chainValid(blockchain.chain)
    if isValid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)