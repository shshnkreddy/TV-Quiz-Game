from socket import *
#from _thread import *
#import threading import Thread 
from random import * 
from select import *
import time

port = 8021
threads_list = []
counter = 0
#print(counter)
conn_list = []
scores_list = []
names_list = []
NUMBER_OF_QUESTIONS = 5
answers_list = []
questions_list =[]
timeout = 60
MAX_SCORE = []
MIN_CONT = 2
asked_questions = []

def broadcast(message):
	for conn in conn_list:
		conn.send(message.encode('ascii'))

def start_contest():
	
	global MAX_SCORE
	global MAX_ALLOWED
	global questions_list
	global asked_questions
	global scores_list
	global NUMBER_OF_QUESTIONS
	 
	NUMBER_OF_QUESTIONS = 4
	MAX_ALLOWED = 3
	MIN_CONT = 2
	questions_list = ["What is greater than 5? \n a) 2 \n b) 7 ", "What is 5 - 2? \n a) 3 \n b) 1", "What is the weather today? \n a) HOT\n b) COLD ", "Will RCB win today? \na) YES \nb) NO", "Which team is the best ipl team? \na) RCB \nb) RCB"]
	answers_list = ["b", "a", "a", "b", "a"]

	for i in range(MIN_CONT):
		scores_list.append(0)

	for i in range(2):
		MAX_SCORE.append(0)

	message = "\nContest Started: \n How to Play; \n 1) Press Enter to hit the buzzer. \n 2) If you hit the buzzer first, you get a chance to answer the question. \n 3) Player to answer " + str(NUMBER_OF_QUESTIONS) + " first wins."
	broadcast(message)
	print(message)

	print(names_list)
	

	while MAX_SCORE[0] < MAX_ALLOWED:
		time.sleep(2)		

		message = "\nScores:"
		broadcast(message)
		for i in range(MIN_CONT):
			#print(i)
			message = "\n" + names_list[i] + ": " + str(scores_list[i])
			broadcast(message)
		
		message = "\n"
		broadcast(message)
		
		question_number = randint(0,NUMBER_OF_QUESTIONS - 1)     
		while(question_number in asked_questions):
			question_number = randint(0, NUMBER_OF_QUESTIONS - 1) 
		asked_questions.append(question_number)                                                      
		
		message = "\nNext Question: " + "\n" + questions_list[question_number]
		broadcast(message)
		print(message)
		message = "\nPress Enter for Buzzer:"
		broadcast(message)

		i = MIN_CONT
		
		#time.sleep(1)

		while i > 0:	
			#time.sleep(0.1)
			buzzed_client, [], [] = select(conn_list,[],[],30)
			i = 0
			l = len(buzzed_client)
			#print("Length of select()", end ="")
			#print(l)
			
			while(l > 0):	
				buzzed_conn = buzzed_client[i]
				
				print("Waiting for key")

				data = buzzed_conn.recv(2048)
				id_number = data.decode('ascii')
				key = int(id_number,10)
				print("Key:", end = "")
				print(key)
				
					
				#time.sleep(5)
				message = "1"
				conn_list[key].send(message.encode('ascii'))
				print("sent buzzer feedback")

				#print(conn_list[key])
				
				print("Waiting for Answer")
				
				data = buzzed_conn.recv(2048)
				ans = data.decode('ascii')

				print("Received an answer:", end = "")
				print(ans) 
				
				if(ans == answers_list[question_number]):
					scores_list[key] = scores_list[key] + 1
					if MAX_SCORE[0] < scores_list[key]:
						MAX_SCORE[0] = scores_list[key]
						MAX_SCORE[1] = key
						message = "\nQuestion answered by participant:" + names_list[key]
						broadcast(message)
					break

				elif ans == "2":
					print("\nTimed Out")
					l -= 1

				else:
					message = "\nWrong Answer"
					conn_list[key].send(message.encode('ascii'))
					print(message)
					l -= 1
				i = i + 1

			else:
				print("\nTimeout, Moving on to next question")	
				break




	message = "\nWinner of the quiz is: " + str(names_list[MAX_SCORE[1]])
	broadcast(message) 
	main()



def waitinglobby(conn):
	if(counter < MIN_CONT):
		message = "Waiting for " + str(MIN_CONT - counter) + " contestant(s)\n"
		conn.send(message.encode())

	if counter == MIN_CONT:
		start_contest()

def main():
	server = socket(AF_INET, SOCK_STREAM)
	server.bind(("",port))
	server.listen(10)
	print("Server is listening")

	while True:
		(conn,addr) = server.accept()
		print("Connection Established")
		print(str(addr))
		conn_list.append(conn)
		conn.setblocking(1)

		global counter 
		global MIN_CONT

		counter = counter + 1 
		MIN_CONT = 2

		if counter <= MIN_CONT:
			#print("\nIn Counter")
			is_connect = "1"                                               #accepting client
			conn.send(is_connect.encode('ascii'))
			
			#message = "Enter you name:"
			#conn.send(message.encode('ascii'))
			
			print("waiting for name")

			data = conn.recv(2048)  

			print("\nReceived Name")                                 #gets name of the user
			
			names_list.append(data.decode('ascii'))    					
			id_number = counter - 1	
			message = str(id_number)									#assigns id number
			conn.send(message.encode('ascii'))
			waitinglobby(conn)
			                        
		else: 
			is_connect = "0"
			conn.send(is_connect.encode('ascii'))                                               #declining client
			conn.send(message.encode('ascii'))
	server.close()


main()





