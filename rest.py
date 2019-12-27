import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys
###wallet imports about rsa needed here
import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP

#import block
import node
import blockchain
import wallet
#import transaction
#import wallet


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK



app = Flask(__name__)
CORS(app)
#blockchain = Blockchain()


#.......................................................................................



# get all transactions in the blockchain

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
	transactions = blockchain.transactions

	response = {'transactions': transactions}
	return jsonify(response), 200
	

@app.route('/id_count/get', methods=['GET'])
def get_id_counts():
	temp = new_node.get_id_count()
	print(temp)
	#a_wallet.balance()
	#response = dict(m =  temp)
	response=[{'id_count': temp}]
	return jsonify(response), 200

@app.route('/register_new_node',methods=['POST'])
def register_node():
	input_json = request.get_json(force=True)
	

	addr=input_json['address']
	pubk=input_json['public_key']
	port=input_json['port']
	
	original_key=RSA.importKey(pubk.encode('ascii'))
	##add check function for params
	
	new_node.current_id_count=new_node.get_id_count()+1
	
	##add node to ring with idc
	idc=new_node.get_id_count()
	new_node.register_node_to_ring(idc,addr,port,pubk)
	response={'id_count':idc}
	
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
	
	#a_wallet=wallet.wallet()
	#a_wallet.balance()
	if(ip=='127.0.0.1'):
		new_node=node.node()
		new_wallet=wallet.wallet(ip)
		new_node.current_id_count=0
	#new_node.create_wallet()
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
		
		r= requests.post(url='http://127.0.0.1:5000/register_new_node',json=parameters)
		result=r.json()
		new_node.current_id_count=result['id_count']
		print(result['id_count'])
		
		#original_key=RSA.importKey(temp.encode('ascii'))
		#print(original_key)
		#if (new_wallet.get_public_key().encrypt("Hello".encode('ascii'),12)==original_key.encrypt("Hello".encode('ascii'),12)):
		#	print("NAIII")
		
			
	app.run(host=ip, port=port)    
