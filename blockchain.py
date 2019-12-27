import block

class blockchain:
 
	def __init__(self):
		self.block_chain = []
		
	def add_block_to_chain(self, block):
		self.block_chain.append(block)
