import socket
import sys
import select
import os

server = socket.socket()

server.connect(('localhost', 7777))

sockets = [sys.stdin, server]
ins, _, _ = select.select(sockets, [], [], 0)
gameStatus = 'connecting'
uid = 0

while gameStatus != 'over':
    for i in ins:
        if i == server:
            if gameStatus == 'connecting':
                uid = int(i.recv(5)[::3])
                gameStatus = 'connected'
            elif gameStatus == 'connected':
                i.recv(4)
        elif i == sys.stdin():
            data = i.recv(4)
            serever.send(bytes(data))
            
