#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

from threading import Thread, Lock;
from encapFramedSock import EncapFramedSock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileThreadServer"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

lock = Lock()
active_files = []

def start_file_transfer(file_name):
    global lock, active_files
    lock.acquire()
    if(file_name in active_files):
        print("File with name already being transferred") 
        lock.release()
        sys.exit(1)
    else:
        active_files.append(file_name)
        lock.release()

def end_file_transfer(file_name):
    global lock, active_files
    lock.acquire()
    active_files.remove(file_name)
    lock.release()
    
class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            try:
                file_name, file_contents = self.fsock.receive(debug)
            except:
                print("Error: failure to transfer file")
                sys.exit(1)
            if debug: print("rec'd: ", file_name)
            if file_name is None:
                print("Error: file name is empty")
                sys.exit(1)
            if file_contents is None:
                print("Error: file contents are empty" )
                sys.exit(1)
            file_name = file_name.decode()
            start_file_transfer(file_name)
            self.write_file(file_name, file_contents)
            end_file_transfer(file_name)

    def write_file(self, file_name, file_contents):
        try:
            if(os.path.exists("./output/"+file_name)):
                print("file with name already exists.")
                sys.exit(1)
            else:
                print("Receiving "  +file_name)
                file_rec = open("./output/"+file_name,"wb")
                file_rec.write(file_contents)
                file_rec.close()
        except FileNotFoundError:
            print("Error: File Not Found")
            sys.exit(1)

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()


