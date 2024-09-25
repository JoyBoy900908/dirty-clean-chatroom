
from lzma import FORMAT_ALONE
import socket
 
# import threading library
import threading
from time import sleep
 
# Choose a port that is free
PORT = 5055
 
# An IPv4 address is obtained
# for the server.
#取得本機ip地址
SERVER = socket.gethostbyname(socket.gethostname()) 
 
# Address is stored as a tuple
ADDRESS = (SERVER, PORT)
 
# the format in which encoding
# and decoding will occur
FORMAT = "utf-8"
 
# Lists that will contains
# all the clients connected to
# the server and their names.
clients, names = [], []
 
# Create a new socket for
# the server
server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
 
# bind the address of the
# server to the socket
server.bind(ADDRESS)
 
# function to start the connection
 
 
def startChat():
 
    print("server is working on " + SERVER)
 
    # listening for connections
    server.listen()
 
    while True:
        conn, addr = server.accept()
        room=conn.recv(1024).decode(FORMAT)
        age=conn.recv(1024).decode(FORMAT)
        age=int(age)

        if room=="dirty":
            if age>=18:
                #connect
             
                # accept connections and returns
                # a new connection to the client
                #  and  the address bound to it
                #conn, addr = server.accept()
                conn.send("NAME".encode(FORMAT))
                # 1024 represents the max amount
                # of data that can be received (bytes)
                name = conn.recv(1024).decode(FORMAT)
                # append the name and client
                # to the respective list
                names.append(name)
                clients.append(conn)
 
                print(f"Name is :{name}")
 
                # broadcast message
                broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))
 
                conn.send('Connection successful!'.encode(FORMAT))
 
                # Start the handling thread
                thread = threading.Thread(target=handle_dirty,
                                          args=(conn, addr))
                thread.start()
 
                # no. of clients connected
                # to the server
                print(f"active connections {threading.activeCount()-1}")

                ######################

            else:
                #close
                connect=False

        elif room=="clean":
            #connect

        ############
            # accept connections and returns
            # a new connection to the client
            #  and  the address bound to it
            conn.send("NAME".encode(FORMAT))
 
            # 1024 represents the max amount
            # of data that can be received (bytes)
            name = conn.recv(1024).decode(FORMAT)
 
            # append the name and client
            # to the respective list
            names.append(name)
            clients.append(conn)
 
            print(f"Name is :{name}")
 
            # broadcast message
            broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))
 
            conn.send('Connection successful!'.encode(FORMAT))
 
            # Start the handling thread
            thread = threading.Thread(target=handle_clean,
                                      args=(conn, addr))
            thread.start()
 
            # no. of clients connected
            # to the server
            print(f"active connections {threading.activeCount()-1}")
 
# method to handle the
# incoming messages
 
 
def handle_clean(conn, addr):
 
    print(f"new connection {addr}")
    connected = True
    dirty_count=0
    while connected:
          # receive message
        message = conn.recv(1024)
        message=message.decode(FORMAT)
        if "fuck" in message:
            message=message.replace("fuck","****")
            dirty_count+=1
            message=message+" warning: violate "+str(dirty_count)
        
        if dirty_count>=3:
            message=message+" is violate 3,out"
            
        message=message.encode(FORMAT)

        # broadcast message
        broadcastMessage(message)
        if dirty_count>=3:
            sleep(2)
            conn.close()
 
    # close the connection
    conn.close()

def handle_dirty(conn, addr):
 
    print(f"new connection {addr}")
    connected = True
 
    while connected:
          # receive message
        message = conn.recv(1024)
        message=message.decode(FORMAT)
        #message=message.replace("fuck","****")
        if "fuck" in message:
            message=message+" (Warning:This is an indecent speech,please pay attention to words and deeds,thanks!)"

        message=message.encode(FORMAT)
        #recvm=message
        #recvm.decode("utf-8")
        #print(type(recvm))
        #recvm=str(recvm)
        #arr=recvm.split(": ")
        #arr[1]=arr[1].replace("'","")
        #print(arr[1])
        #message=arr[0].encode("utf-8")+arr[1].encode("utf-8")
        
         # broadcast message
        broadcastMessage(message)
 
    # close the connection
    conn.close()
 
# method for broadcasting
# messages to the each clients
 
 
def broadcastMessage(message):
    for client in clients:
        client.send(message)
 
 
# call the method to
# begin the communication
startChat()