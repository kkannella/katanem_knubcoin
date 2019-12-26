import socket 
from _thread import *
import threading
##lock declaration , multiple locks multiple purposes
print_lock = threading.Lock()
send_id_lock = threading.Lock()
##global variable declaration 
id_cmax=1

def send_id(c):
	global id_cmax
	#attemp to lock---
	send_id_lock.acquire()
	##send id
	c.send((str(id_cmax)).encode('ascii'))
	##increment for next node
	id_cmax=id_cmax+1
	##release lock---
	send_id_lock.release()

def threaded(c):
	ida=send_id(c)
	while True:
		data = c.recv(1024)
		if not data:
			print('Bye')
			#print_lock.release()
			break
		c.send(data)
	c.close()
		
def Main():
	#id_cmax defines next node id
	##bootstrap node ip/port 
	host='127.0.0.1'
	port = 1339
	
	##classic we use tcp and ipv4
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	##10 default , 1 should work too
	s.listen(10)
	print("Listening for connections on ")
	while True:
		c,addr =s.accept()
		
		#print_lock.acquire()
		print('Connection from :',addr[0],' : ',addr[1])
		##start thread for that connection
		start_new_thread(threaded,(c,))
	s.close()

if __name__=='__main__':
	id_cmax=1
	Main()
