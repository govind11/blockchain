'''
@author: Govind Karmakar
@date: 3 Jun'18
'''
import json
import time
from hashlib import sha256


class Block(object):
	def __init__(self, index, transactions, timestamp, previousHash):
		self.index = []
		self.transactions = transactions
		self.timestamp = timestamp
		self.previousHash = previousHash

	def compute_hash(self):
		'''
		   A function that creates the hash of the block
		'''
		blockString = json.dumps(self.__dict__, sort_keys=True)
		return sha256(blockString.encode()).hexdigest()


class BlockChain(object):
	DIFFICULTY = 0

	def __init__(self):
		self.unconfirmedTransactions = []  # data yet to get in blockchain
		self.chain = []
		self.create_genesis_block()

	def create_genesis_block(self):
		'''
		   Method to generate block and appends it to the chain.
		   The block has index 0, previous hash as 0, and a valid hash.
		'''
		genesisBlock = Block(0, [], time.time(), '0')
		genesisBlock.hash = genesisBlock.compute_hash()
		self.chain.append(genesisBlock)

	@property
	def last_block(self):
		return self.chain[-1]

	def proof_of_work(self, block):
		'''
		   Method tries different values of nonce to get a hash
		   that satisfies the difficulty criteria.
		'''
		block.nonce = 0
		computeHash = block.compute_hash()
		while not compute_hash.startswith('0' * self.DIFFICULTY):
			block.nonce += 1
			computedHash = block.compute_hash()
		return computedHash

	def add_block(self, block, proof):
		'''
		   Method to add blocks after verification.
		'''
		if previousHash != block.previousHash:
			return False
		if not self.is_valid_proof(block, proof):
			return False
		block.hash = proof
		self.chain.append(block)
		return True

	def is_valid_proof(self, block, blockHash):
		'''
		   Check if blockHash of the block satisfies the difficulty creteria.
		'''
		return (blockHash.startswith('0'*self.DIFFICULTY) and
			blockHash == block.compute_hash())

	def add_new_transaction(self, transaction):
		'''
		   Method to add new transaction.
		'''
		self.unconfirmedTransactions.append(transaction)

	def mine(self):
		'''
		   Method serves as an identification to add the pending transactions
		   to the blockchain and adding them to the block and figuring out the
		   proof of work.
		'''
		if not self.unconfirmedTransactions:
			return False
		lastBlock = self.last_block
		newBlock = Block(index=lastBlock.index+1,
						 transactions=self.unconfirmedTransactions,
						 timestamp=time.time(),
						 previousHash=lastBlock.hash)
		proof = self.proof_of_work(newBlock)
		self.add_block(newBlock, proof)
		self.unconfirmedTransactions = []
		return newBlock.index
