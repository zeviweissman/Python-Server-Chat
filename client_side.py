# socket lets you open a socket
import socket

# Thread lets you to run a few functions simultaneously
from threading import Thread

# sleep is used to have a pause between code lines
from time import sleep

# to start you need to enter the servers ip and port
address = "?.?.?.?"
port = ?

# here you start the socket and connect to the server
# were gonna use the default connection (AF_INET = ipv4) and (SOCK_STREAM = TCP)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, port))

# this function checks if the client is a member
def member_check():
    member = input("are you a member: ")
    while member not in ("yes", "no"):
        member = input("are you a member: ")
    return member

# if the client is not a member this function will ask him for is sign up info
def sign_up(member):
    if member == "no":
        sign_in = [input("user first name: \n"), input("user last name: \n"), input("user name: \n"), input("password: \n"), input("renter password: \n")]
        while sign_in[3] == sign_in[4]:
            print("welcome yamelech")
            break
        else:
            print("the passwords are not the same\n renter your info:")
            sign_in = [input("user first name: \n"), input("user last name: \n"), input("user name: \n"), input("password: \n"), input("renter password: \n")]
# here we send is info to the server (we have a sleep between the sends because we want them to be sent separately)
        client.send("new user".encode())
        sleep(2)
        client.send(sign_in[2].encode())
        sleep(2)
        client.send(sign_in[3].encode())

# if the client is a member this function will ask him for is login info info and then sends it to the server
    else:
        login_info = [input("user name:\n"), input("password:\n")]
        client.send("old user".encode())
        sleep(2)
        client.send(login_info[0].encode())
        sleep(2)
        client.send(login_info[1].encode())

# here we actually run the functions
sign_up(member_check())

#  if he receives welcome it means that the info is right and he could start chatting
while client.recv(1024).decode() == "welcome":
    break

# if he doesn't receive the welcome that means there is a error and we close the connection and restart the program
else:
    print("wrong name or password try again")
    client.close()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((address, port))

    sign_up(member_check())


# after we finish the sign in we will have two codes running the all time one for sending messages and one for receiving messages for that we will use the Thread function
def send_message():
    while True:
        client.send(input().encode())


t1 = Thread(target=send_message)
t1.start()

while True:
    print(client.recv(1024).decode())


