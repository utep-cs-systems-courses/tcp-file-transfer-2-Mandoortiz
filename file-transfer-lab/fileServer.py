#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileServer"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)
while True:
    
    sock, addr = lsock.accept()    
    print("connection rec'd from", addr)

    if not os.fork():
        try:
            file_name, file_contents = framedReceive(sock, debug)
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
