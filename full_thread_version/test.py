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
	total_time=0
	total_list=[]
	total_block_time=0
	total_block_list=[]
	for j in blockaki:
		print("This block index is",j.index)
		for i in range (len(j.listOfTransactions)):
			print(j.listOfTransactions[i].sender_address," --> ",j.listOfTransactions[i].recipient_address," : ",j.listOfTransactions[i].amount)
			total_time=total_time + (j.listOfTransactions[i].finish - j.listOfTransactions[i].elapsed)
			total_list.append(j.listOfTransactions[i].finish - j.listOfTransactions[i].elapsed)
		total_block_time= total_block_time + (j.finish-j.timestamp)
		total_block_list.append(j.finish-j.timestamp)
	print("Average Time for transactions was:" , total_time / len(total_list))
	print("Average Time for blocks was:" , total_block_time / len(total_block_list))
	

