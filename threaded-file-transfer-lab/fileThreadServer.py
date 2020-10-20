#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

from threading import Thread;
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

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            #payload = self.fsock.receive(debug)
            #if debug: print("rec'd: ", payload)
            #if not payload:     # done
            #    if debug: print(f"thread connected to {addr} done")
            #    self.fsock.close()
            #    return          # exit
            #payload += b"!"             # make emphatic!
            #self.fsock.send(payload, debug)
            try:
                file_name, file_contents = self.fsock.receive(debug)
            except:
                print("Error: failure to transfer file")
                sys.exit(1)
            if debug: print("rec'd: ", file_name)
            if file_contents is None:
                print("Error: file is empty")
                sys.exit(1)
            file_name = file_name.decode()
            if(os.path.exists("./output/"+file_name)):
                print("file with name already exists.")
                sys.exit(1)
            else:
                print("Receiving "  +file_name)
                file_rec = open("./output/"+file_name,"wb")
                file_rec.write(file_contents)
                file_rec.close()
while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()


