import blockchain
import time

class Block:
	def __init__(self,index,prvHash):
		##set
		self.index=index	
		self.previousHash=prvHash
		self.timestamp=time.time()
		self.nonce=0
		self.listOfTransactions=[]
		self.hash=(str(self.index)+str(self.previousHash)+str(self.timestamp)+str(self.nonce)+str(self.listOfTransactions)).encode('ascii')
		
	def myHash(self,noncea):
		self.nonce=nocnea
		self.hash=(str(self.index)+str(self.previousHash)+str(self.timestamp)+str(noncea)+str(self.listOfTransactions)).encode('ascii')
		#calculate self.hash
		return self.hash

	def add_transaction(self, transaction):
		self.listOfTransactions.append(transaction)
		#add a transaction to the block
