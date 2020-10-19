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
    try:
        sock, addr = lsock.accept()
    except:
        print("Error: failure to transfer file")
        sys.exit(1)
        
    print("connection rec'd from", addr)

    if not os.fork():
        payload = framedReceive(sock, debug)
        if debug: print("rec'd: ", payload)
        
        if payload is None:
            print("Error: file is empty")
            sys.exit(1)
        payload = payload.decode()
        file_name = payload.split("%^&")[0]
        file_contents = payload.split("%^&")[1]

        if(os.path.isfile(file_name)):
            print("file with name already exists.")
        else:
            print("Receiving "  +file_name)
            file_rec = open(file_name,"w")
            file_rec.write(file_contents)
            file_rec.close()
