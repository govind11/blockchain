'''
@author: Govind Karmakar
@date: 3 Jun'18
'''
from block import BlockChain as BlockChain
from flask import Flask, request
import requests
import time


app = Flask(__name__)

# The node's copy of blockchain
blockChain = BlockChain()


@app.route('/newTransaction', methods=['POST'])
def new_transaction():
	txData = request.get_json()
	requiredFields = ['author', 'content']
	for field in requiredFields:
		if not txData.get(field):
			return 'Invalid transaction data.', 404
	txData['timestamp'] = time.time()
	blockChain.add_new_transaction(txData)
	return 'Succss', 201

@app.route('/chain', methods=['GET'])
def get_chain():
	chainData = []
	for block in blockChain.chain:
		chainData.append(block.__dict__)
	return json.dumps({'length': len(chainData),
					   'chain': chainData})

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
	result = blockChain.mine()
	if not result:
		return 'No transaction to mine.'
	return 'Block #{} is mined.'.format(result)

# endpoint to query confirmed transactions
@app.route('/pendingTransactions')
def get_pendng_transactions():
	return json.dumps(blockChain.unconfirmedTransactions)



if __name__ == '__main__':
	app.run(debug=True, port=8000)
