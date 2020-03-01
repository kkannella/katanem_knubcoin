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
def node0_trans():
	print("Active 0")
	for i in range (5):
		parameters={'recipient_node':i,'amount':1}
		ra = requests.post(url='http://127.0.0.1:5000/create_transactiona',json=parameters)
		result=ra.json()
		print("node 0 did trans :", i , "result :",result['comp'])

def node1_trans():
	print("Active 1")
	for i in range (5):
		parameters={'recipient_node':i,'amount':1}
		ra = requests.post(url='http://127.0.0.2:5000/create_transactiona',json=parameters)
		result=ra.json()
		print("node 1 did trans :", i , " result :",result['comp'])

def node2_trans():
	print("Active 2")
	for i in range (5):
		parameters={'recipient_node':i,'amount':1}
		ra = requests.post(url='http://127.0.0.3:5000/create_transactiona',json=parameters)
		result=ra.json()
		print("node 2 did trans :", i , " result :",result['comp'])

def node3_trans():
	print("Active 3")
	for i in range (5):
		parameters={'recipient_node':i,'amount':1}
		ra = requests.post(url='http://127.0.0.4:5000/create_transactiona',json=parameters)
		result=ra.json()
		print("node 3 did trans :", i , " result :",result['comp'])

def node4_trans():
	print("Active 4")
	for i in range (5):
		parameters={'recipient_node':i,'amount':1}
		ra = requests.post(url='http://127.0.0.5:5000/create_transactiona',json=parameters)
		result=ra.json()
		print("node 4 did trans :", i , " result :",result['comp'])

if __name__ == '__main__':
	print("Starting test")
	
	start_new_thread(node0_trans,())
	start_new_thread(node1_trans,())
	start_new_thread(node2_trans,())
	start_new_thread(node3_trans,())
	start_new_thread(node4_trans,())

	
	time.sleep(10)

