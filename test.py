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
	blockaki=tempa[-1]
	for i in range (len(blockaki.listOfTransactions)):
		print(blockaki.listOfTransactions[i].recipient_address)
		
	ra = requests.get(url='http://127.0.0.2:5000/get_block')
	result=ra.json()
	block=result['block']
	tempa= jsonpickle.decode(block)
	blockaki=tempa[-1]
	for i in range (len(blockaki.listOfTransactions)):
		print(blockaki.listOfTransactions[i].recipient_address)
	
	ra = requests.get(url='http://127.0.0.3:5000/get_block')
	result=ra.json()
	block=result['block']
	tempa= jsonpickle.decode(block)
	blockaki=tempa[-1]
	for i in range (len(blockaki.listOfTransactions)):
		print(blockaki.listOfTransactions[i].recipient_address)
	
	ra = requests.get(url='http://127.0.0.4:5000/get_block')
	result=ra.json()
	block=result['block']
	tempa= jsonpickle.decode(block)
	blockaki=tempa[-1]
	for i in range (len(blockaki.listOfTransactions)):
		print(blockaki.listOfTransactions[i].recipient_address)
	ra = requests.get(url='http://127.0.0.5:5000/get_block')
	result=ra.json()
	block=result['block']
	tempa= jsonpickle.decode(block)
	blockaki=tempa[-1]
	for i in range (len(blockaki.listOfTransactions)):
		print(blockaki.listOfTransactions[i].recipient_address)

