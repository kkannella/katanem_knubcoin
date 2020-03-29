import blockchain
import time

from _thread import *
import threading
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
		self.used_utxo=[]
		self.created_utxo=[]
		#no point to include the 2 below
		self.nonce=0
		self.hash=None
		self.hash_digest=""
		self.block_lock=threading.Lock()
		self.time_sign=0
		#self.prevhash_digest=prvHash.hexdigest()
		
	def myHash(self,noncea):
		
		self.nonce=noncea
		self.hash=SHA.new((str(self.index)+str(self.previousHash)+str(self.timestamp)+str(self.nonce)).encode())
		##self.hash=SHA.new((str(self.index)+str(self.previousHash)+str(self.timestamp)+str(self.nonce)+str(self.listOfTransactions)).encode())
		#calculate self.hash this one must match difficulty params
		self.hash_digest = self.hash.hexdigest()
		
		return self.hash

	def add_transaction(self, transaction):
		self.listOfTransactions.append(transaction)
		#add a transaction to the block
