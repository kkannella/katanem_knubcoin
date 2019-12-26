import socket
import sys
def Main(argv):
	host ='127.0.0.1'
	port = 1339
	
	s_host=argv[0]
	s_port=int(argv[1])
	
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((s_host,s_port))
	s.connect((host,port))
	
	message = "Hello from client "
		
	while True:
		s.send(message.encode('ascii'))
		data = s.recv(1024)
				
		print("Receive from server :", str(data.decode('ascii')))
		
		
		ans=input('\nContinue(y/n) :')
		if ans == 'y':
			continue
		else:
			break
	
	s.close()
if __name__ == "__main__":
   Main(sys.argv[1:])
