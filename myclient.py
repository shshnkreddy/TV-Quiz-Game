# Import socket module 
from socket import *  
from select import *
port = 8021  
host = gethostname()
import sys

def Main(): 
    
    print("Welcome")
    name = input("Enter your name: ")

    client = socket(AF_INET,SOCK_STREAM)
    client.connect((host,port))
    data = client.recv(2048)
    #print(data.decode('ascii'))
    #print("Received is_connect")                       #Receives a bool if client can connect to server
    
    is_connect = 0
    if data.decode('ascii') == "1":
        is_connect = 1
       # lst, [], [] = select([sys.stdin],[],[],10)
        #if(len(lst) > 0 and lst[0] == sys.stdin):
            #print("Name Entered")
       #message = raw_input()
        client.send(name.encode('ascii'))
        #print("sent name")

        #else:
            #print("watiting for you to enter name")
    else:
        is_connect = 0
        #print("is_connect = 0")

    data = client.recv(2048)
    id_number = data.decode('ascii')
    #print("id_number:", end = "")
    #print(id_number)

    while is_connect:     
        #print("Waiting for input")
        readable,[],[] = select([sys.stdin, client], [], [],30)
        #print("Got data")
        #print(readable[0])
        #print("readable:")
        #print(readable[0])

        
        if(len(readable) > 0):
            if(readable[0] == sys.stdin and len(readable) > 0):
                x = input()
                message = id_number
                client.send(message.encode('ascii'))
                print("Sent Buzzer")
                #client.recv(2048)
                #print("reached continue")
                continue

            if(readable[0] == client and len(readable) > 0):
                data = client.recv(2048)
                #print(data.decode('ascii'))
                message = data.decode('ascii')
                if message == "1":
                        print("You have 30s to answer the question")
                        read, [], [] = select([sys.stdin], [], [], 30)
                        if(len(read) > 0):
                            ans = input()
                            client.send(ans.encode('ascii'))
                        else:
                            print("Timed out")
                            ans = "2"
                            client.send(ans.encode('ascii'))

                else:
                    print(message)
        else:
            print("Game Over")
            client.close()
            exit()
          
    if is_connect == 0:
        print("Game has enough contestants, try again")
        client.close()

    client.close()

if __name__ == '__main__': 
    Main() 