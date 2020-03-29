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
	ra = requests.get(url='http://127.0.0.1:5000/get_chain')
	result=ra.json()
	chain=result['chain']
	tempa= jsonpickle.decode(chain)
	listaki = tempa.block_chain
	for i in range (len(listaki)):
		print(listaki[i].index)
