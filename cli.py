import argparse
import sys
import jsonpickle
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

parser = argparse.ArgumentParser(description='Commands parser')
parser.add_argument('command', type=str, nargs="+" ,help='Command string : [t <recipient adress in ip format> <amount in int or float>] , [view] , [balance]')
###switch statemnet for each command depends on command
args = parser.parse_args()
print(args)
com =args.command
if (com[0]=="view"):
	##reject if nargs >2
	if (len(com)>1):
		print("Usage")
	else:
		ra = requests.get(url='http://127.0.0.1:5000/get_block')
		result=ra.json()
		block=result['block']
		tempa= jsonpickle.decode(block)
		blockaki=tempa[-1]
		for i in (blockaki.listOfTransactions):
			print(i.sender_address," --> ",i.recipient_address," : ",i.amount)
	
elif (com[0]=="t"):
	if (len(com)!=3):
		print("Usage")
	else:
	##demand nargs == 3
		#check for ip format 
		recip_addr = com[1]
		if(not(validate_ip(recip_addr))):
			print("Invalid ip")
			sys.exit(1)
		#check for int format or float		
		amount = int(com[2])
		
		parameters={'recipient_node':recip_addr,'amount':amount}
		ra = requests.post(url='http://127.0.0.1:5000/create_transactiona_from_cli',json=parameters)
		result=ra.json()
		print(result['comp'])
		

elif (com[0]=="balance"):
	if(len(com)>1):
		print("Usage")
	##same as case0
	else:
		###find a way to define local ip on netwrk
		ra = requests.get(url='http://127.0.0.1:5000/get_balance')
		result=ra.json()
		balance=result['balance']
		print("My balance is:",balance)

