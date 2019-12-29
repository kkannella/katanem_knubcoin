import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys
###wallet imports about rsa needed here
import binascii
from _thread import *
import threading

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP

import time
import block
import node
import blockchain
import wallet
import transaction
import jsonpickle
### JUST A BASIC EXAMPLE OF A REST API WITH FLASK

apply_lock = threading.Lock()
sync_lock = threading.Lock()

app = Flask(__name__)
CORS(app)


##-----thread functions
def b_cast(ip_list,port_list,addr):
	##Add loop checking for status 200
	time.sleep(2)
	for i in range (len(ip_list)):
		temp_r= requests.get(url="http://"+ str(ip_list[i]) + ":"+ str(port_list[i]) +"/check_live")
		while	(temp_r.status_code != 200):
			time.sleep(0.5)
			temp_r= requests.get(url="http://"+ str(ip_list[i]) + ":"+ str(port_list[i]) +"/check_live")
	##Send post requests to all nodes
	temp_obj=new_node.chain
	temp_chain = jsonpickle.encode(temp_obj)

	parameters={'ring_id':new_node.ring_id, 'ring_ip':new_node.ring_ip,'ring_port':new_node.ring_port,'ring_pubk':new_node.ring_public_key,'block_chain':temp_chain }

	for i in range (len(ip_list)):
		r_b_cast= requests.post(url="http://"+ str(ip_list[i]) + ":"+ str(port_list[i]) +"/apply_lists",json=parameters)
		result=r_b_cast.json()
	
	##sent to new node coins
	time.sleep(2)
	new_node.create_transaction(ip,new_wallet.private_key,addr,100)
	print("Finished thread")
#.......................................................................................

@app.route('/add_transaction',methods=['POST'])
def add_transactions():
	input_json = request.get_json(force=True)
	temp_trans=input_json['transaction']
	transactionb= jsonpickle.decode(temp_trans)
	##call verify
	if(new_node.validate_transaction(transactionb)):
		print("VALID")
	##add to block if verified
	print(transactionb.sender_address)
	response={'comp':1}
	return jsonify(response), 200
	
@app.route('/get_transactions',methods=['GET'])
def get_transactions():
	temp=new_node.ring_ip
	response={'test_list':temp}
	return jsonify(response), 200

@app.route('/apply_lists',methods=['POST'])
def apply_list():
	input_json = request.get_json(force=True)
	
	#apply_lock.acquire()
	id_list=input_json['ring_id']
	ip_list=input_json['ring_ip']
	pubk_list=input_json['ring_pubk']
	port_list=input_json['ring_port']
	b_chain=input_json['block_chain']
	
	new_node.ring_id=id_list
	new_node.ring_ip=ip_list
	new_node.ring_port=pubk_list
	new_node.ring_public_key=port_list
	new_node.chain=jsonpickle.decode(b_chain)
	#apply_lock.release()
	response={'id_count':99}

	return jsonify(response), 200


# get all transactions in the blockchain

@app.route('/check_live', methods=['GET'])
def check_life():
	response={'live':1}
	return jsonify(response), 200




@app.route('/register_new_node',methods=['POST'])
def register_node():
	input_json = request.get_json(force=True)

	addr=input_json['address']
	pubk=input_json['public_key']
	port=input_json['port']

	#original_key=RSA.importKey(pubk.encode('ascii'))
	
	##add check function for params

	new_node.current_id_count=new_node.get_id_count()+1

	##add node to ring with idc
	idc=new_node.get_id_count()
	new_node.register_node_to_ring(idc,addr,port,pubk)
	response={'id_count':idc}
	
	##broadcast ring list with thread function
	start_new_thread(b_cast,(new_node.ring_ip,new_node.ring_port,addr))
	
	
	
	#welcome_trans=transaction.Transaction(ip,new_wallet.private_key,addr,100)
	
	return jsonify(response), 200


#@app.route('/')
# run it once fore every node

if __name__ == '__main__':

	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('-i', '--ip', default='127.0.0.1', type=str, help='ip to setup')
	parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
	args = parser.parse_args()
	port = args.port
	ip=args.ip

	
	if(ip=='127.0.0.1'):
		new_node=node.node()
		new_wallet=wallet.wallet(ip)
		new_node.current_id_count=0
		##set node params
		new_node.ring_id.append(0)
		new_node.ring_ip.append(ip)
		new_node.ring_port.append(port)
		new_node.chain=blockchain.blockchain()
		public_key_string=new_wallet.get_public_key().exportKey("PEM").decode('ascii')
		new_node.ring_public_key.append(public_key_string)

		##Create genesis block
		print("Starting gen block")

		gen_block=new_node.create_new_block(0,1)
		#gen_trans=new_node.create_transaction()
		gen_trans=transaction.Transaction(ip,new_wallet.private_key,ip,500)
		gen_block.add_transaction(gen_trans)
		#add block to blockchain as its finished
		print("Adding first block to bchain")
		new_node.chain.add_block_to_chain(gen_block)
		print("finished gen block")
		##add gen block to blockchain

	else:
		new_node=node.node()
		#pass ip as param
		new_wallet=wallet.wallet(ip)
		#print(new_wallet.get_public_key())
		public_key_string=new_wallet.get_public_key().exportKey("PEM")
		#print(public_key_string)
		#original_key=RSA.importKey(public_key_string)
		#print(original_key)
		#temp = public_key_string.decode('ascii')

		##Pass bublic key address and port
		parameters={'public_key':public_key_string.decode('ascii'), 'address':new_wallet.get_address(),'port':port }

		r = requests.post(url='http://127.0.0.1:5000/register_new_node',json=parameters)
		result=r.json()
		new_node.current_id_count=result['id_count']
		print(result['id_count'])

		#original_key=RSA.importKey(temp.encode('ascii'))
		#print(original_key)
		#if (new_wallet.get_public_key().encrypt("Hello".encode('ascii'),12)==original_key.encrypt("Hello".encode('ascii'),12)):
		#	print("NAIII")

	app.run(host=ip, port=port)
