import blockchain
import time


import Crypto
import Crypto.Random

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5



class Block:
	def __init__(self,index,prvHash):
		##set
		self.index=index	
		self.previousHash=prvHash
		self.timestamp=time.time()
		self.listOfTransactions=[]
		#no point to include the 2 below
		self.nonce=0
		self.hash=0

		
	def myHash(self,noncea):
		self.nonce=nocnea
			self.hash=SHA.new((str(self.index)+str(self.previousHash)+str(self.timestamp)+str(self.nonce)).encode())
		##self.hash=SHA.new((str(self.index)+str(self.previousHash)+str(self.timestamp)+str(self.nonce)+str(self.listOfTransactions)).encode())
		#calculate self.hash this one must match difficulty params
		return self.hash

	def add_transaction(self, transaction):
		self.listOfTransactions.append(transaction)
		#add a transaction to the block
