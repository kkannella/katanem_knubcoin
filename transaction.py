from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template

import random
import wallet

class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value):

        ##set
        #self.sender_address: To public key του wallet από το οποίο προέρχονται τα χρήματα
        self.sender_address=sender_address
        #self.recipient_address: To public key του wallet στο οποίο θα καταλήξουν τα χρήματα
        self.recipient_address=recipient_address
        #self.amount: το ποσό που θα μεταφερθεί
        self.amount=value
        #self.transaction_id: το hash του transaction
        myid=(str(sender_address)+str(recipient_address)+str(value)+str(random.random())).encode()
        self.transaction_id=SHA.new(myid)
        self.transaction_temp=myid
        #self.transaction_inputs: λίστα από Transaction Input
        #self.transaction_inputs=transaction_in
        #self.transaction_outputs: λίστα από Transaction Output
        self.transaction_id_digest=self.transaction_id.hexdigest()
        #selfSignature
        self.signature=PKCS1_v1_5.new(sender_private_key).sign(self.transaction_id)
