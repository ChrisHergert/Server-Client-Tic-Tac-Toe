from socket import *
import time
import sys
import select
import os
import string
import time

def printSend(connfd,player,msg):
	connfd.send(msg)
	print player,">",msg
def createBoard(moves):
	brd = "\n  board\n  1 2 3\n +-+-+-\nA|"+moves[0]+"|"+moves[1]+"|"+moves[2]+"\n +-+-+-\nB|"+moves[3]+"|"+moves[4]+"|"+moves[5]+"\n +-+-+-\nC|"+moves[6]+"|"+moves[7]+"|"+moves[8]+"\n"
	return brd
def sendAll(cdx,cdo,msg):
	print("X>"+msg)
	cdo.send(msg)
	print("O>"+msg)
	cdx.send(msg)
def youWin(cdx,cdo,winner):
	if winner == cdx:
		printSend(cdx,"X","You win, O resigned\n")
		exit()
	if winner == cdo:
		printSend(cdo,"O","You win, X resigned\n")
		exit()
def notYou(cd, player):
	printSend(cd,player,"It's not your turn")
def sendHelp(cd,player):
	printSend(cd,player,"?-Display this help\nR-Resign\nMove<R><C>-Move where <R> is a row A, B, C and <C> is a column 1,2, or 3\n Example Moves: MA1 MC3 MB1")
def rowify(r):
	if (r=="A"): return 0
	elif(r=="B"): return 1
	elif(r=="C"): return 2
	else: return -1
def colify(c):
	if(c=="1"): return 0
	elif(c=="2"): return 1
	elif(c=="3"): return 2
	else: return -1
def posify(r,c):
	return ((3*r)+c)
def isValid(move):
	if((len(move)==4) and (move[0] == 'M') and move[3]=='\n'):
		r = rowify(move[1])
		c = colify(move[2])
		if((move[0]=='M') and (r >= 0) and (c >= 0)):
			return ((r*3)+c)
		else:
			return -1
	else:
		return -1
def sendOutTheBoard(cdx,cdo,moves,turn,both):
	brd=createBoard(moves)
	if (both==True):
		printSend(cdx, "X", brd+"\nPlease enter a move")
		printSend(cdo,"O", brd+"\nPlease enter a move")
	else:
		if(cdx==turn):
			printSend(cdx,"X",brd)
			printSend(cdx,"X","Your turn")
			printSend(cdo,"O",brd)
		elif(cdo==turn):
			printSend(cdo,"O",brd)
			printSend(cdo,"O","Your turn")
			printSend(cdx,"X",brd)
def winCheck(m):
	if(m[0]==m[1]==m[2]!=" "): return 1
	elif(m[3]==m[4]==m[5]!=" "): return 1
	elif(m[6]==m[7]==m[8]!=" "): return 1
	elif(m[0]==m[3]==m[6]!=" "): return 1
	elif(m[1]==m[4]==m[7]!=" "): return 1
	elif(m[2]==m[5]==m[8]!=" "): return 1
	elif(m[0]==m[4]==m[8]!=" "): return 1
	elif(m[2]==m[4]==m[6]!=" "): return 1
	else: return -1


os.system("clear")
print "Network server starting"
moves = [" "," "," "," "," "," "," "," "," "]


s = socket(AF_INET,SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(("",int(sys.argv[1]))) # Bind to port named in cmdline arg
s.listen(5)

print "Waiting on clients"

clx,addrx = s.accept()
print "X<Connected"
printSend(clx,"X","You are player X. Waiting on player O")

clo,addro = s.accept()
print "O<Connected"
printSend(clo,"O","You are player O\n")
players = {clx:"X",clo:"O"}

clo.send("Game beginning\n")
clx.send("Game beginning\n")

clients = [clx,clo] # list of all active clients
turns = 0
c = 0
whoseturn=clx
sendOutTheBoard(clx,clo,moves,whoseturn,False)
while (turns < 9) and (c < 50):
	input,output,err = select.select(clients,[],[])
	for i in input:
		if i == clo:
			buf = i.recv(1024)
			print("X<"+buf)

			if whoseturn==clo:
				if not buf: break

				checkMove=isValid(buf)

				if buf == "R\n":
					youWin(clx,clo,clx)
				elif buf == "?\n":
					sendHelp(i,"O")
				elif (checkMove >= 0):
					if(moves[checkMove] == " "):
						moves[checkMove] = "O"
						turns=turns+1
						whoseturn=clx
						sendOutTheBoard(clx,clo,moves,whoseturn,False)
						if(winCheck(moves)==1):
							printSend(clo,"O","You win")
							printSend(clx,"X","You lose")
							time.sleep(1)
							exit()
					else:
						printSend(i,"O","That spot is not open")
				else:
					i.send("Your turn")
			else:
				notYou(i,"X")

		elif i == clx:
			buf = i.recv(1024)
			print("O<"+buf)

			if whoseturn == i:
				if not buf: break
			
				checkMove = isValid(buf)

				if buf == "R\n":
					youWin(clx,clo,clo)
				elif buf =="?\n":
					sendHelp(i,"X")
				elif (checkMove >= 0):
					if moves[checkMove] == " ":
						moves[checkMove] = "X"
						turns=turns+1
						whoseturn=clo
						sendOutTheBoard(clx,clo,moves,whoseturn,False)
						if(winCheck(moves)==1):
							printSend(i,"X","You win")
							printSend(clo,"O","You lose")
							time.sleep(1)
							exit()
					else:
						i.send("That spot is not open")
				else:
					i.send("Your turn")
			else:
				notYou(i,"O")
		c=c+1
		if(turns == 9):
			sendAll(clx,clo,"Tie Game")
#
s.close()
