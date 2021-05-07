import socket, sys, select

socket_server = socket.socket()
server_host = socket.gethostname()
ip = socket.gethostbyname(server_host)
sport = 7777
server_host = input('Enter server\'s IP address: ')
socket_server.connect((server_host, sport))
print('connection succesful...')
sockets = [sys.stdin.fileno(), socket_server.fileno()]
while True:
    ins, _, _ = select.select(sockets, [], [], 0)
    for i in ins:
        if i is sys.stdin.fileno():
            socket_server.send(bytes(sys.stdin.readline().encode()))
        elif i is socket_server.fileno():
            indata = socket_server.recv(1024)
            if not indata:
                sockets.pop(1)
                socket_server.close()
            else:
                print(indata)