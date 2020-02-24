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
	parameters={'recipient_node':1,'amount':10}
	ra = requests.post(url='http://127.0.0.1:5000/create_transactiona',json=parameters)
	result=ra.json()
	print(result['comp'])
