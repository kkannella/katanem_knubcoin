import block

from _thread import *
import threading

class blockchain:
 
	def __init__(self):
		self.block_chain = []
		self.chain_lock=threading.Lock()
	def add_block_to_chain(self, block):
		##add block to chain
		self.block_chain.append(block)
