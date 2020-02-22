import block
import wallet
import blockchain
import transaction
import Crypto
import Crypto.Random
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



##-----thread functions
def b_cast_t(ip_list,port_list,transa):
	temp_obj = jsonpickle.encode(transa)
	parameters={'transaction':temp_obj}
	for i in range (len(ip_list)):
		b_cast_transa= requests.post(url="http://"+ str(ip_list[i]) + ":"+ str(port_list[i]) +"/add_transaction",json=parameters)
		result=b_cast_transa.json()


class node:

	def __init__(self):
		self.NBC=0 ##test
		##set
		self.wallet=None
		self.chain=None
		#self.NBCs
		self.UTXOs = []
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
		self.UTXOs.append([])

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
		#use of signature and NBCs balance
		sender_adress=transaction.sender_address
		##use temp until h is passed humanly
		h= SHA.new(transaction.transaction_temp)
		signature=transaction.signature
		
		pubkey=RSA.importKey(self.ring_public_key[self.ring_ip.index(sender_adress)].encode('ascii'))
		
		####error with h, sig 
		##dev note ti skata pezi me to h kai to jsonpickle , neo tropo to pass obj mallon
		verified = PKCS1_v1_5.new(pubkey).verify(h, signature)
		
		return verified

	def add_transaction_to_block(self,transaction,block,capacity):
		
		#if enough transactions  mine
		block.add_transaction(transaction)
		if(len(block.listOfTransactions)==capacity):
			print("error")
			
			####thread#####
			#thread########
			########thread#
			#mine_block()


	def mine_block(self , block,difficulty):
		trynonce = 0
		print("Mining Block")
		while (not(tryhash=block.myHash(trynonce).hexdigest().startswith('0'* difficulty)) ):
			trynonce = trynonce +1
		print("Block mined")
		##add broadcast block
		
		return 1


	def broadcast_block(self , block):
		
		return 1



##	def valid_proof(.., difficulty=MINING_DIFFICULTY):
##		return 1

	def validate_block(self, block,blockchain,difficulty):
		prvHash=block.previousHash
		myHashStr=block.hash.hexdigest()
		##
		##temp_bits= str(bin(int(block.hash.hexdigest()[0], base=16)))
		##first_dif_bits = int(temp_bits[2:difficulty+2])
		prvhash2=blockchain.block_chain[-1].hash
		if((prvHash!=prvhash2) or (not(myHashStr.startswith('0' * difficulty)))):
			return False #invalid block
		else:
			return True #valid block
	#concencus functions

	def valid_chain(self, chain,difficulty):
		mychain=chain
		for i in range(2,len(mychain)+1): ##starts from 2 coz 1 is gen block
			if(not(validate_block(mychain[i],mychain,difficulty))):
				return False
		return True

	def resolve_conflicts(self):
		#resolve correct chain
		return 1

	def get_id_count(self):
		return self.current_id_count
