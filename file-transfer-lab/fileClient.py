#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)
while True:
    file_name = input("Enter name of file: ")
    file_name = file_name.strip()
    if(len(file_name) == 0 or file_name.lower() == "exit"):
        # Allow for user to exit if they want to
        print("Goodbye")
        sys.exit(0)
    try:
        # Check that file exists
        file_in = open(file_name,"rb")             
        file_contents = file_in.read()                  
        if(len(file_contents) == 0):
            # Check that file is not a zero length file
            print("Error: File is empty.")
            continue
        print("sending ", file_name)
        framedSend(s, file_name, file_contents, debug)
    except FileNotFoundError:
        print("Error: File Not Found.")
        sys.exit(1)
