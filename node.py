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
#chain_lock = threading.Lock()

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
		self.UTXO = []
		self.current_id_count=0
		self.ring_id=[] #make new list we will add nodes later
		self.ring_ip=[]
		self.ring_port=[]
		self.ring_public_key=[]
		self.ring_balance=[]
		#slef.ring[]   #here we store information for every node, as its id, its address (ip:port) its public key and its balance
	
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
		##search UTXO for the transaction inputs
		total_available = 0
		to_delete=[]
		for utxo_iter in  (self.UTXO):
			if (utxo_iter[2]==transaction.sender_address):
				total_available = total_available + utxo_iter[3]
				to_delete.append(utxo_iter)
				if(total_available >= transaction.amount):
					break
		if(total_available >= transaction.amount):
			##delete used utxos 
			for utxo_iter in (to_delete):
				self.UTXO.remove(utxo_iter)
			##create UTXOs
			if(total_available > transaction.amount):
				resta = total_available-transaction.amount
				self.unique_id=self.unique_id+1
				self.UTXO.append((self.unique_id,transaction.transaction_id_digest,transaction.sender_address,resta))
			else:
				resta=0
			self.unique_id=self.unique_id+1
			self.UTXO.append((self.unique_id,transaction.transaction_id_digest,transaction.recipient_address,transaction.amount))
			validate_lock.release() ##lock to serialize transactions
			return True
		
		validate_lock.release()
		return False

	def add_transaction_to_block(self,transaction,block,capacity):
		#if enough transactions mine
		block.add_transaction(transaction)
		if(len(block.listOfTransactions)==capacity):
			#spawn thread to mine block
			#start_new_thread(miner_job,(block,)) 
			#ama den gini me thread isos kalitera?
			self.mine_block(block,1)
			self.current_block = self.create_new_block(block.index+1,block.hash_digest)	
		##validate_lock.release() ##lock to serialize transactions
		return 1

	def mine_block(self , block,difficulty):
		trynonce = 0
		print("Mining Block")
		while (not(block.myHash(trynonce).hexdigest().startswith('0'* difficulty)) ):
			trynonce = trynonce + 1
		print("Block mined")
		##add broadcast block
		#self.broadcast_block(block)
		start_new_thread(self.broadcast_block,(block,))
		print("Broadcasted")
		##create new block to chain
		##self.chain.block_chain.append(self.create_new_block(block.index+1,block.hash))
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
	#concencus functions

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
		if(len(new_chain.block_chain)==len(self.chain.block_chain) ):
			return 1
			
		elif(len(new_chain.block_chain)>len(self.chain.block_chain)):
			self.chain = new_chain
			return 0
			
	def get_id_count(self):
		return self.current_id_count
