#!/usr/local/bin/python3

'''
Authur:        Tarrell Fletcher
Date Created : January 17, 2017
Email:         Tarrell13@verizon.net

Program Name: TheChat

Synopsis: Program will allow chat capabilities between clients. Program is multithreaded, which allows
multiple connections to the server.

Log: May be kinks when exiting the program. Still need to fully handle all exceptions but program is functional.
'''

import socket
import platform
import threading
import sys
import time
import os

'''Define Globals'''
HOST = ""
PORT = 25000
ADDR = (HOST, PORT)
CONNECTION_LIST = []
PLATFORM = platform.system()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

'''Connect Client to the Server'''
def client_connect():

    try:
        server_ip = input("[+] Server's IP to connect to: ")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client.connect((server_ip, PORT))
            print("[+] Connected to Server at address: %s" %client.getpeername()[0])
        except:
            print("[*] No Server Listening at Specified Address")
            sys.exit()

        client_dump_thread = threading.Thread(target=client_dump, args=(client,))
        client_dump_thread.start()
        communicate(client)
        client.close()
        client_dump_thread.exit()
        sys.exit()

    except:
        print("[*] Disconnected from Server")
        sys.exit()


'''Threaded loop to continue listening for new connections'''
def server_loop():

    server.bind(ADDR)
    server.listen(10)

    print("[*] Server started on %s" %platform.node())

    try:
        while True:
            client_socket, client_addr = server.accept()
            CONNECTION_LIST.append(client_socket)
            dump_thread = threading.Thread(target=dump, args=(client_socket,))
            dump_thread.start()
            print("\r[+] New Connection from: %s" %client_addr[0])
    except:
        server.send("[*] Server at %s is now Offline" %platform.node())
        server.close()
        sys.exit()


'''Server Host Connect Back'''
def self_connect():

    try:
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect(("localhost", 25000))
        client_dump_thread = threading.Thread(target=client_dump, args=(sc,))
        client_dump_thread.start()
        communicate(sc)
    except:
        sys.exit()

    sys.exit()

def communicate(client):

    try:
        while True:
            time.sleep(0.5)
            data = input("> ")
            client.send(str.encode("[%s] => %s" %(os.getlogin(), data)))
    except KeyboardInterrupt:
            client.send(str.encode("[*] %s has left the chat room" %os.getlogin()))
            client.close()
            sys.exit()
    except:
        print("[*] Error - Program Terminating")
        client.close()
        sys.exit()

def dump(client):
    try:
        while True:
            data = client.recv(1024)
            for sock in CONNECTION_LIST:
                if sock != server and sock != client:
                    sock.send(data)
    except:
        CONNECTION_LIST.remove(client)
        client.close()

def client_dump(client):
    while True:
        try:
            print(client.recv(1024).decode("utf-8")+"\r")
        except:
            client.close()
            sys.exit()

def main():

   server_thread = threading.Thread(target=server_loop)

   while True:

       try:
            print("Select Operating Mode")
            print("---------------------")
            print("1. Server Mode")
            print("2. Client Mode")
            mode = int(input("Enter mode of operation: "))
            print("\n\n")
            if mode in [1,2]:
                break
            else:
                raise ValueError
       except ValueError:
           print("Enter either (1) for Server or (2) for Client")


   if mode == 1:
       try:
            server_thread.start()
            time.sleep(1)
            self_connect()
       except:
           sys.exit()

   elif mode == 2:
       try:
           client_connect()
       except:
           sys.exit()


main()
