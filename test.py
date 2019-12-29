import jsonpickle
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS


		
if __name__ == '__main__':

	r_b_cast= requests.get(url="http://127.0.0.4:5000/get_transactions")
	result=r_b_cast.json()
	print(result['test_list'])

