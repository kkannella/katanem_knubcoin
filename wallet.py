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
		#self.public_key
		#self.private_key
		self.public_key=self.private_key.publickey()
		self.address=addr
		#self.transactions

	def balance(self):
		print(self.private_key)
		print(self.public_key)
		key=self.private_key
		p_key=key.publickey()
		message='hello world'
		message=str.encode(message)
		cipher = PKCS1_OAEP.new(p_key)
		ciphertext = cipher.encrypt(message)
		print(ciphertext)
		cipher = PKCS1_OAEP.new(key)
		message = cipher.decrypt(ciphertext)
		print(message.decode())
				
	def get_public_key(self):
		return self.public_key
	
	def get_address(self):
		return self.address
