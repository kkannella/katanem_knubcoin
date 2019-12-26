import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys

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

@app.route('/test', methods=['GET'])
def get_test():
	temp= a_wallet.get_return()
	a_wallet.balance()
	#response = dict(m =  temp)
	response={'hi':"hello"}
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
	
	a_wallet=wallet.wallet()
	a_wallet.balance()
	a_node=node.node()
	a_node.create_wallet()
	
	if(ip!='127.0.0.1'):
		r = requests.get(url='http://127.0.0.1:5000/test')	
		print(r.status_code)
		print(r.json())
	app.run(host=ip, port=port)
    
