import jsonpickle
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
		
if __name__ == '__main__':
	ra = requests.get(url='http://127.0.0.1:5000/get_block')
	result=ra.json()
	block=result['block']
	tempa= jsonpickle.decode(block)
	blockaki=tempa
	for j in blockaki:
		print("This block index is",j.index)
		for i in range (len(j.listOfTransactions)):
			print(j.listOfTransactions[i].sender_address," --> ",j.listOfTransactions[i].recipient_address," : ",j.listOfTransactions[i].amount)
		

