import jsonpickle
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import sys
import binascii
from _thread import *
import threading
import time
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-id', '--id', default='0', type=str, help='my id')
args = parser.parse_args()
my_id=args.id

file_trs = open("transactions"+str(int(my_id)-1)+".txt", "r")
itera=0
for x in file_trs:
	itera= itera + 1
	#send from numba to i node monies
	tokens = x.split()
	recipient_id = int(tokens[0][-1]) 	
	amount = int(tokens[1])
	parameters={'recipient_node':recipient_id,'amount':amount}
	ra = requests.post(url='http://127.0.0.'+str(my_id)+':5000/create_transactiona',json=parameters)
	result=ra.json()
	print("node did trans : result :",itera)
	#time.sleep(0.4)
	
file_trs.close()
