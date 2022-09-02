from http.client import EXPECTATION_FAILED
from logging import exception
import threading
import socket
import sys

from pip import main
# 1: connect to the server, if failed do it again, if more than
# several times, then exit. done 
# 2: left server --- done
# 3: if input incorrect done
# 4: porter < 1024 done 

# set localhost and port
host = '127.0.0.1' 

if len(sys.argv) != 2:
    print("Please get one input for port.")
    sys.exit()
else:
    port = int(sys.argv[1])
    
    port_not_work = True
    # used exist port
    while port_not_work:
        if port < 1024:
            port = int(input("Please choose new port."))
        else:
            port_not_work = False
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
except:
    print("Error to create the socket!")
    sys.exit()
          
try:
    
    server.bind((host,port))
    server.listen()
    print("Server is doing its job...")
except:
    for each_try in range(0,3):
        try:
            server.bind((host,port))
            not_SUCCESS = False
            print("Connected!")
        except:
            print("The server is not able to bind.")
            print( str(each_try) + " time trying to connect again...")
            not_SUCCESS = True      
    if not_SUCCESS:
        print("Meet the maximum trying time")
        sys.exit()

clients = []
usernames = []

def globalMessage(message,client):
    for person in clients:
        try:
            person.send(message)
        except:
            client.close()
            username = usernames[clients.index(client)]
            message = username + " has left the server."
            print(message)
            clients.remove(client)
            client.close()
            globalMessage(message.encode('ascii'))
            usernames.remove(username)
            break

def checkClient(client):
    while True:
        try:
            message = client.recv(1024)
            if not len(message):
                raise Exception
            else:
                globalMessage(message,client)
        except:
            username = usernames[clients.index(client)]
            message = username + " has left the server."
            print(message)
            clients.remove(client)
            client.close()
            globalMessage(message.encode('ascii'),client)
            usernames.remove(username)
            break

def main():
    while True:
        client,address = server.accept()
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)
        serverMessage = username + " has joined in the server. The hostname is " + str(address[0]) + ", the port is: " + str(address[1])
        print(serverMessage)
        welcomeMessage = username + " has joined in the server."
        globalMessage(welcomeMessage.encode('ascii'),client)
        client.send('\n You have pushed into the server!!!!'.encode('ascii'))
        thread = threading.Thread(target=checkClient, args=(client,))
        thread.start()
    
main()

    
        
        
        
        