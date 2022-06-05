# socket lets you open a socket
import socket

# select lets you to handle the traffic between the client and the server
import select

# login is a python page that we wrote it as a few functions that were gonna use later on
from function import *

# to start you need to enter the servers ip and port
address = "?.?.?.?"
port = ?

# here you open the socket and start listening to accept clients
# were gonna use the default connection (AF_INET = ipv4) and (SOCK_STREAM = TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((address, port))
server.listen()
print("server listening")

# two variable that we use later to store the clients
sockets_list = [server] # note you want to already have in the list the server
user_names = {} # this dict. will have as keys all the sockets and as values all the user names

# this function receives the message and who sent it so it could send the message to everybody besides the sender
def notify_all(msg, non_receptors):
# the function iterates through the sockets_list and if the socket is not the sender or the server it sends him the message
    for connection in sockets_list:
        if connection not in non_receptors:
            connection.send(msg)

# this function receives the new user and tells him who is online
def greet(client):
    user_list = []
# the function iterates through the sockets_list and if the socket is not the new client and not the server it gets there user name from the user dictionary and sends it to the client
    for sockets in sockets_list:
        if sockets is not client and sockets is not server:
            for key, value in user_names.items():
                if key == sockets:
                    user_list.append(value)
    greet_msg = f"\nhello {name}! \n users online: " + str(user_list)
    client.send(greet_msg.encode())

# this function finds a user name by getting its socket address
# and checking it the user dict.
def user_check():
# the function iterates through the sockets_list and makes sure its not the server who sent it
# and if so it checks the socket who sent it in the user dictionary and returns what user sent the message
    for socket in sockets_list:
        if socket is sockets and socket is not server:
            for key, value in user_names.items():
                if key == socket:
                    return value



# at first were gonna put all the sockets in the select function so it could manage the connection
# the select function takes 3 arguments readable, writable, exceptional were only gonna use the readable and leave the rest empty
# and were running the code with try just in case the client closes the connection on is side so theres no error
while sockets_list:
    try:
        readable, _, _ = select.select(sockets_list, [], [])

# this for loop checks  if a new connection is happening or someone is sending a message
        for sockets in readable:

# if its a new connection it connects
            if sockets is server:
                client, address = server.accept()

# if the client is a new user it runs the new_user function
                while client.recv(1024).decode() == "new user":
                    print("new user")

# and we save the user in the user dict. and in the sockets_list
                    name = new_user(client.recv(1024).decode(), client.recv(1024).decode())
                    user_names[client] = name
                    client.send("welcome".encode())
                    sockets_list.append(client)
                    print(f'connected to {name}')

# and we let him know who's online
                    greet(client)

# and we notify all the clients online that he joined
                    notify_all(f"client {name} entered".encode(), [server, client])
                    break

# if the client is a old user it runs the login function
                else:
                    print("old user")
                    name = login(client.recv(1024).decode(), client.recv(1024).decode())

# if the login info is wrong it sends the client a notification
                    if name == "not user":
                        client.send("wrong name or password try again".encode())
                        pass

# if the login is correct we save the user in the user dict. and in the sockets_list
                    else:
                        user_names[client] = name
                        client.send("welcome".encode())
                        sockets_list.append(client)
                        print(f'connected to {name}')

# and we let him know who's online
                        greet(client)

# and we notify all the clients online that he joined
                        notify_all(f"client {name} entered".encode(), [server, client])
                    pass

# this else is in a case that there wasn't a connection so now we check if someone either is sending a message or closing the connection
            else:

# we try to see if its a message
                try:
                    data = sockets.recv(1024)

# if its a message that's not empty we send it out to everyone but if its empty it means its not a message
# because you cant send empty messages therefore it means someone is disconnecting
                    if data.decode() != '':
                        notify_all(str(user_check() + " says: " + data.decode()).encode(), [server, sockets])

# for some reason when i run the code on my local network it worked perfectly but then when i tested it on a real server a few problems accrued
# the problems had to do with the server getting separate packets of data as one packet of data while i was trying to debug it i found out that
# if i put this error where it separates the data packets and there sent separately so that's why i use the time function without importing it
                    else:
                        time.sleep(20)
                        pass

# in case of exception that means someone is disconnecting
                except Exception as e:
                    print(e)
                    print(f"user {user_check()} BYE")
# this tells all the other clients who left
                    notify_all(f"user {user_check()} left".encode(), [server, sockets])
                    sockets_list.remove(sockets)
                    sockets.close()

# this is a general exception on the all code so the server doesn't stop if there's a error
    except Exception as ee:
        print(ee)
