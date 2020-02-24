import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4



class wallet:

	def __init__(self,addr):
		##set
		self.private_key=RSA.generate(1024)
		self.public_key=self.private_key.publickey()
		self.address=addr
		#self.transactions

	def balance(self,UTXOs):
		balance=0
		#public_key_string=self.get_public_key().exportKey("PEM")
		for itera in UTXOs:
			print(str(itera[2]))
			print(str(self.address))
			#print(public_key_string)
			#print("PRoblem :",itera[2])
			if (str(itera[2])==str(self.address)):
				balance= balance + itera[3]
				print("FOUND ONE")
		return balance
			
	def get_public_key(self):
		return self.public_key
	
	def get_address(self):
		return self.address
