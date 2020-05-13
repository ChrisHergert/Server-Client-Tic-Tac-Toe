from socket import *
import sys
import select
import os

os.system("clear")

s = socket(AF_INET,SOCK_STREAM)

try:
	s.connect((sys.argv[1], int(sys.argv[2])))
	for i in range(2):
		buf=s.recv(1024)
		print buf
except:
	print "Connection error: address not valid"
	sys.exit(0)
sockets = [sys.stdin,s]
c = 0 #Prevent infinite loops
while True:
#	buf = raw_input("Please enter a command")
#	s.send(buf)
	inputs,outputs,err = select.select(sockets,[],[])

	for i in inputs:
		if i==s:
			buf = i.recv(1024)
			if not buf:
				print "Disconnected from server"
				exit()
			else:
				print buf
		else:
			buf = sys.stdin.readline()
			s.send(buf)
	if((buf=="You lose") or (buf=="You win")):
		exit()
#
s.close()
