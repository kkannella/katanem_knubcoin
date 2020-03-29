import socket 
from _thread import *
import threading
import sys
import selectors

ultra_lock = threading.Lock()

def threaded(s,ip_list,port_list,id_cmax):
	while True:
		c,addr =s.accept()
		ultra_lock.acquire()
		print('Connection from :',addr[0],' : ',addr[1])
		data = s.recv(1024)
		if str(data.decode('ascii'))!='':
			print("Receive from server :", str(data.decode('ascii')))
			ultra_lock_release()
			print("Bye")
			break
		print("Bye")
	c.close()
		
def Main():
	#id_cmax defines next node id
	##bootstrap node ip/port 
	host='127.0.0.1'
	l_port = 1336
	c_port= 1337
	N=2
	id_cmax=1;
	
	test_transa=[2,3,2]
	test_amount=[2,4,6]
	
	l_ip_list=[] #list of listening ips
	l_port_list=[] #list of listeing ports 
	c_port_list=[] #list of connecting ports , ips stay the same
	
	l_ip_list.append(host)
	l_port_list.append(l_port)
	c_port_list.append(c_port)
	
	s_listen = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s_listen.bind((host,l_port))
	s_listen.listen(10)
	
	s_connect = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s_connect.bind((host,c_port))
	
	
	conn=[] ##list contain connection
	addrs=[] ##list contains addresses
	temp=0
	print("Listening :")
	for itera in range (N):
		c,addr =s_listen.accept()
		conn.append(c)
		addrs.append(addr)
		print('Connection from :',addr[0],' : ',addr[1])
		l_ip_list.append(addr[0])
		l_port_list.append(addr[1])
		id_cmax=id_cmax+1
		#data =c.recv(1024) #receive ip,port
		#c.send((str(id_cmax)).encode('ascii'))
	for itera in range (N):
		c=conn[itera]
		c.send((str(id_cmax)+" "+str(l_ip_list)+" "+str(l_port_list)).encode('ascii'))
		c.close
	print("done sending data to all")	
	##-----
	print("Listening for transa thread")
	#start_new_thread(threaded,(s_listen,l_ip_list,c_port_list,id_cmax))
	for i in range (len(test_transa)):
		print(i)
		s_connect.connect((l_ip_list[i],l_port_list[i]))
		message = "Sending  "+str(test_amount[i])
		s_connect.send(message.encode('ascii'))
		s_connect.close()
		s_connect = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s_connect.bind((host,c_port+1))
if __name__=='__main__':
	Main()
