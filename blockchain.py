import block

class Blockchain:
 
	def __init__(self):
		self.unconfirmed_transactions = [] # data yet to get into blockchain
		self.block_chain = []
		self.create_genesis_block()
		
	def add_block_to_chain(self, block):
		self.block_chain.append(block)
