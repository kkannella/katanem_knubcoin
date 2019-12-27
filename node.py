import block
import wallet
import blockchain

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
class node:

	def __init__(self):
		#self.NBC=100?
		##set
		self.wallet=None
		#self.chain
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

	def create_transaction(sender, receiver,signature):
		#remember to broadcast it

		return 1

	def broadcast_transaction():

		return 1


	def validate_transaction(self,transaction):
		#use of signature and NBCs balance
		sender_adress=transaction.sender_address
		h=transaction.transaction_id
		signature=transaction.signature
		pubkey=RSA.importKey(self.ring_public_key[self.ring_ip.index(sender_adress)].encode('ascii'))
		try:
			PKCS1_v1_5.new(pubkey).verify(h, signature)
			return True
		except(ValueError,TypeError):
			return False

	def add_transaction_to_block(transaction,block,capacity):
		#if enough transactions  mine
		block.add_transaction(transaction)
		if(len(block.listOfTransactions)==capacity):
			####thread#####
			#thread########
			########thread#
			mine_block()


	def mine_block():
		return 1


	def broadcast_block():
		return 1



##	def valid_proof(.., difficulty=MINING_DIFFICULTY):
##		return 1

	def validate_block(block,blockchain,difficulty):
		prvHash=block.previousHash
		myHash=block.hash
		temp_bits= str(bin(int(block.hash.hexdigest()[0], base=16)))
		first_dif_bits = int(temp_bits[2:difficulty+2])
		prvhash2=blockchain.block_chain[-1].hash
		if((prvHash!=prvhash2) or (first_dif_bits != 0)):
			return False #invalid block
		else:
			return True #valid block
	#concencus functions

	def valid_chain(self, chain,difficulty):
		myc=chain.block_chain
		for i in range(1,len(myc)):
			if(not(validate_block(myc[i],[myc[i-1]],difficulty))):
				return False
		return True

	def resolve_conflicts(self):
		#resolve correct chain
		return 1

	def get_id_count(self):
		return self.current_id_count
