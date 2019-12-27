import blockchain
import time

class Block:
	def __init__(self,index,prvHash):
		##set
		self.index=index	
		self.previousHash=prvHash
		self.timestamp=time.time()
		#self.hash
		self.nonce=0
		self.listOfTransactions=[]
		
	def myHash():
		self.hash=1
		#calculate self.hash


	##def add_transaction(transaction transaction, blockchain blockchain):
	##	self.hash=2
		#add a transaction to the block
