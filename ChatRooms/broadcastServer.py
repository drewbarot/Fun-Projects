# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 22:43:52 2019

@author: Drew
"""

"""

Requirements: Python 3.5

This is the most basic version of the chat server. All it
allows is a server to run, and for clients to join the 
server.

This is the most vanilla version. It only allows for a message
to be received and broadcast to all other listeners. Think of
each client as an Oberver of all other clients, except the server.

The first client opened acts as the server, and only tracks
who has joined. Subsequent clients who are added will be
able to message to the server, and the server will broadcast
the client's messages to other active clients. 

To launch this on Windows:
1) Open CMD and navigate to the directory where the file is. Use cd
2) When in the folder, first type broadcastServer.py, which launches the server
3) The server won't display anything yet. Instead, open a new CMD window,
    navigate to the folder again with cd. 
4) When in the folder, type in telnet localhost 7777
    Note that telnet is a type of way to connect to another party, like server
5) Repeat this for as many clients as you want. As they are added, they'll be
    shown on the server CMD window, which must remain open. 
6) For each client window, go in and hit enter twice (do to avoid localecho)
7) Now, you are free to type in any client window. It will be pushed to others.

This is very basic, and can be expanded. 

"""

# Import the sockets library to run on a socket on a given IP. Sockets allow
# applications to run on a defined space on an IP.
import socket

# Import the threads library to run each client on a seperate thread. Threads
# allow your program to execute multiple things as once by partioning the CPU.
import threading

# We will create a socket object called mySocket. This will allow us to use
# sockets for each client. We will use the Python library we implemented. We
# can ignore most of the syntaactical components here, just know that we are
# establishing a TCP IP socket. 
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We bind the socket object we created to an IP-the localhost here (127.0.0.1)
# We also use port 10000 for the port to run the server on this socket. 
mySocket.bind(('127.0.0.1', 7777))

# Socket becomes active, and listens for connectors. Runs servers.
mySocket.listen(1)

# We create a Python list structure to store the connections for the server. 
connectionsList = []

# Now, we create a function to be invoked for each client that joins. One 
# function will be launched on one thread for each cient. 
def clientManager(c, a):
    # Declare the global connectionsList variable in the function.
    global connectionsList
    # Always run this function.
    while True:
        # Allow data to be recieved as bytes (1024 bytes)
        data = c.recv(1024)
        # Whenever someone types, publish to server.
        print("Character typed")
        # For each connection in the server's list of connections, broadcast
        # a client's message to all other clients.
        for connection in connectionsList:
            # Weird format to make this work because localecho is broken in CMD
            if not(str(connection)[-7:-2]==str(a)[-6:-1]):
                # Send the bytes out.
                connection.send(bytes(data))
        # If data recieved isn't real data (keyboard interrupt), quit server
        if not data:
            # Remove from server's list, and close the thread. 
            connectionsList.remove(c)
            c.close()
            break
        
# We can get to our "main" method. This is what we invoke when we run the
# program itself, and it calls the functions we need. It always runs.
while True:
    # Accept a client (c) and a ID (a)
    c, a = mySocket.accept()
    # Create a thread from the threading library for each client connecting.
    # Each thread launches an instance of the clientManager function w/ args
    cThread = threading.Thread(target = clientManager, args=(c,a))
    # Allow everything to run is background.
    cThread.daemon = True
    # Start the thread. 
    cThread.start()
    # Add the client to the list of connections
    connectionsList.append(c)
    # Print connected message to server when client connects 
    print("Connected!")
    # Print the connection details. 
    print(connectionsList)
