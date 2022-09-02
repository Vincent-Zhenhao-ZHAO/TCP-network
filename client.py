import socket
import threading
import sys
  
try:
    username = sys.argv[1]
    hostname = sys.argv[2]
    port = int(sys.argv[3])
except:
    print("please give 3 values: username, hostname and port")
    sys.exit()

port_not_work = True
while port_not_work:
    if port < 1024:
        port = int(input("Please choose new port."))
    else:
        port_not_work = False
        
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((hostname,port))
except:
    print("Unable to connect! Please check the port and host.")    
    sys.exit()    
        
# 1: connect with the port, try(except) done
# 2: receive - try(except) done
# 3: input port/username/hostname -> try(except) done

# choose to use TCP and IPV4 socket

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
        except:
            print("The server is down, please connct again")
            client.close() 
            break
        
def write():
    while True:
        try:
            message = username + ": " + input("")
            client.send(message.encode('ascii'))
        except:
            print("The server is down, please connct again")
            client.close() 
            break

client.send(username.encode('ascii')) 
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
              

