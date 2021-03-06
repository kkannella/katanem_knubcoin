import block
import wallet
import blockchain
import transaction
import Crypto
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP

import jsonpickle

import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from _thread import *
import threading
validate_lock = threading.Lock()
transaction_lock = threading.Lock()

##-----thread functions
def b_cast_t(ip_list,port_list,transa):
	temp_obj = jsonpickle.encode(transa)
	parameters={'transaction':temp_obj}
	for i in range (len(ip_list)):
		b_cast_transa= requests.post(url="http://"+ str(ip_list[i]) + ":"+ str(port_list[i]) +"/add_transaction",json=parameters)
		result=b_cast_transa.json()

def miner_job(block):
	mine_block(block,difficulty)
	return 1


class node:

	def __init__(self):
		self.NBC=0 ##test
		##set
		self.unique_id=31
		self.wallet=None
		self.chain=None
		self.current_block=None
		self.prev_block=None
		self.UTXO = []
		self.current_id_count=0
		self.ring_id=[] #make new list we will add nodes later
		self.ring_ip=[]
		self.ring_port=[]
		self.ring_public_key=[]
		self.ring_balance=[]
		self.completed_transactions=[] #list of transaction_id_digest
		self.fat_lock = threading.Lock()
	
	def create_new_block(self,index,prvHash):
		return block.Block(index,prvHash)

	def create_wallet(self):
		self.wallet=wallet.wallet()
		#create a wallet for this node, with a public key and a private key

	def register_node_to_ring(self,idc,ip,port,pubk):
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
		self.ring_id.append(idc)
		self.ring_ip.append(ip)
		self.ring_port.append(port)
		self.ring_public_key.append(pubk)
		##self.UTXOs.append([])

	def create_transaction(self, sender_address, sender_private_key, recipient_address, value):
		new_trans=transaction.Transaction(sender_address,sender_private_key,recipient_address,value)
		#remember to broadcast it
		self.broadcast_transaction(new_trans)
		return 1
		
	def broadcast_transaction(self,transaction):
		print("Broadcasting Transaction")
		##Send post requests to all nodes
		##broadcast ring list with thread function
		start_new_thread(b_cast_t,(self.ring_ip,self.ring_port,transaction))
		
	def validate_transaction(self,transaction):
		validate_lock.acquire()
		#use of signature and NBCs balance
		sender_adress=transaction.sender_address
		##use temp until h is passed humanly
		h= SHA.new(transaction.transaction_temp)
		signature=transaction.signature
		pubkey=RSA.importKey(self.ring_public_key[self.ring_ip.index(sender_adress)].encode('ascii'))
		####error with h, sig 
		##dev note ti skata pezi me to h kai to jsonpickle , neo tropo to pass obj mallon
		verified = PKCS1_v1_5.new(pubkey).verify(h, signature)
		if (not(verified)):
			validate_lock.release()
			return False
		##Search if transaction already happened
		
		for trans_iter in self.completed_transactions:
			if(transaction.transaction_id_digest == trans_iter.transaction_id_digest):
				##duplicate transaction 
				validate_lock.release()
				return False
					
		##search UTXO for the transaction inputs
		total_available = 0
		to_delete=[]
		# either self.UTXO if new block  or current_block.created_utxo
		#the magic starts with prev_block
		if ((len(self.current_block.created_utxo)==0) and (self.prev_block==None)):
			for utxo_iter in  (self.UTXO):
				self.current_block.created_utxo.append(utxo_iter)
		elif (len(self.current_block.created_utxo)==0):
			#for utxo_iter in  (self.UTXO):
			for utxo_iter in (self.prev_block.created_utxo):
				self.current_block.created_utxo.append(utxo_iter)		
		
		# or current_block.created_utxo if alreaddy new block
		
		for utxo_iter in (self.current_block.created_utxo):
			if (utxo_iter[2]==transaction.sender_address):
				total_available = total_available + utxo_iter[3]
				to_delete.append(utxo_iter)#utxos used used by this block
				#self.current_block.created_utxo.remove(utxo_iter) #utxos used used by this block
				if(total_available >= transaction.amount):
					break
			
		if(total_available >= transaction.amount):
			resta = total_available-transaction.amount
			if(resta>0):
				self.unique_id=self.unique_id+1
				self.current_block.created_utxo.append((self.unique_id,transaction.transaction_id_digest,transaction.sender_address,resta))
			self.unique_id=self.unique_id+1
			self.current_block.created_utxo.append((self.unique_id,transaction.transaction_id_digest,transaction.recipient_address,transaction.amount))	
			##actually delete utxos
			for utxo_iter in to_delete:	
				self.current_block.created_utxo.remove(utxo_iter)
				
		else:
			validate_lock.release()
			return False	
		validate_lock.release()
		return True
		
	def add_transaction_to_block(self,transaction,block,capacity):
		#if enough transactions mine
		block.add_transaction(transaction)
		if(len(block.listOfTransactions)==capacity):
			#spawn thread to mine block
			#start_new_thread(miner_job,(block,)) 
			#ama den gini me thread isos kalitera?
			self.mine_block(block,4)
			self.prev_block = block
			self.current_block = self.create_new_block(block.index+1,block.hash_digest)	
		##validate_lock.release() ##lock to serialize transactions
		return 1

	def mine_block(self , block,difficulty):
		trynonce = 0
		print("Mining Block")
		while (not(block.myHash(trynonce).hexdigest().startswith('0'* difficulty)) ):
			trynonce = trynonce + 1
		print("Block mined")
		start_new_thread(self.broadcast_block,(block,))
		return 1


	def broadcast_block(self , block):
		temp_block = jsonpickle.encode(block)
		parameters={'block':temp_block}
		for i in range (len(self.ring_ip)):
			b_cast_block= requests.post(url="http://"+ str(self.ring_ip[i]) + ":"+ str(self.ring_port[i]) +"/add_block",json=parameters)
			result=b_cast_block.json()
		return 1


	def validate_block(self, block,blockchainlist,difficulty):
		prvHash=block.previousHash
		myHashStr=block.hash_digest
		print("Printg prevhash :",prvHash)
		prvhash2=blockchainlist[-1].hash_digest
		print("Printg prevhash2 :",prvhash2)
		if((prvHash==prvhash2) and (myHashStr.startswith('0' * difficulty))):
			return 1 #valid block
		elif ((prvHash!=prvhash2)):
			return 2 #invalid block due to change in chain
		else:
			return 3 #invalid due to errors

	def valid_chain(self, chain,difficulty):
		mychain=chain.block_chain
		for i in range(2,len(mychain)+1): ##starts from 2 coz 1 is gen block
			if(not(validate_block(mychain[i],mychain,difficulty))):
				return False
		return True

	def resolve_conflicts(self):
		#resolve correct chain
		#request chain length from everyone
		for i in range (len(self.ring_ip)):
			req_chain= requests.get(url="http://"+ str(self.ring_ip[i]) + ":"+ str(self.ring_port[i]) +"/get_chain")
			result=req_chain.json()
			temp_chain=result['chain']
			new_chain = jsonpickle.decode(temp_chain)
			##acquire lock on chain struct !!!!
			self.fat_lock.acquire()
			if (len(new_chain.block_chain)>len(self.chain.block_chain)):
				#copy state from the new chain
				self.UTXO = []
				self.UTXO = new_chain.block_chain[-1].created_utxo.copy()
				self.chain.block_chain = new_chain.block_chain.copy()
			self.fat_lock.release()	
		return 0
			
	def run_block_transactions(self, block):
		##search  for the transaction inputs
		validate_lock.acquire()
		self.fat_lock.acquire()
		self.UTXO=[]
		#add transactions to completed pool
		for tran_iter in block.listOfTransactions: 
			self.completed_transactions.append(tran_iter)
		#manage utxos to respect new order
		#for utxo_iter in (block.used_utxo):
			#pezi na ine kai ola edo
			#self.UTXO.remove(utxo_iter)
			##problem arises if new_block has started to be filled?
		for utxo_iter in (block.created_utxo):
			self.UTXO.append(utxo_iter)
		validate_lock.release()
		self.fat_lock.release()
		return 0			
	def get_id_count(self):
		return self.current_id_count
