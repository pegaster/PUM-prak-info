import socket
import sys
import select
server = socket.socket()
server.bind((‘localhost’, 7777))
server.listen(15)
clients = []
gameStatus = 'connecting'
msgs = {}
addrs = {}
sockets = [sys.stdin, server]
ins, _, _ = select.select(sockets, [], [], 0)
for i in ins:
    if i is server: 
	    conn, addres = server.accept()
      print(f'{addres} is connected')
      msgs[conn] = ""
      addrs[conn] = addres
	  elif i is sys.stdin:
	    if gameStatus == 'connecting':
        gameStatus = 'start'
      elif gameStatus == 'start':
        gameStatus == 'paused'
        print('Do you want to quit game? y/n')
      elif gameStatus == 'paused':
        data = i.readline()
        if data == 'n':
          gameStatus = 'start'
        elif data == 'y':
          break
      else:
        users[i] = recv(4)
        if users[i] == None:
          print(f'{addrs[i]} disconnected')
          user.pop(i)
          addrs.pop(i)
print('Game quited')
