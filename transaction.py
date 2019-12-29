from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template

import random
import wallet

class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value ):


        ##set
        #self.sender_address: To public key του wallet από το οποίο προέρχονται τα χρήματα
        self.sender_address=sender_address
        #self.recipient_address: To public key του wallet στο οποίο θα καταλήξουν τα χρήματα
        self.recipient_address=recipient_address
        #self.amount: το ποσό που θα μεταφερθεί
        self.amount=value
        #self.transaction_id: το hash του transaction
        myid=(str(sender_address)+str(recipient_address)+str(value)+str(random.random())).encode('ASCII')
        self.transaction_id=SHA256.new(data=myid)
        #self.transaction_inputs: λίστα από Transaction Input
        self.transaction_inputs=[]
        #self.transaction_outputs: λίστα από Transaction Output
        self.transaction_outputs=[]
        #selfSignature
        self.signature=PKCS1_v1_5.new(sender_private_key).sign(self.transaction_id)





    def to_dict(self):
       return 1

#    def sign_transaction(self):
#       return 1
