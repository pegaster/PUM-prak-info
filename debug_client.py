import socket, sys, select

socket_server = socket.socket()
server_host = socket.gethostname()
ip = socket.gethostbyname(server_host)
sport = 7777
server_host = input('Enter server\'s IP address: ')
socket_server.connect((server_host, sport))
print('connection succesful...')
sockets = [socket_server]
while True:
    ins, _, _ = select.select(sockets, [], [], 0)
    for i in ins:
        if i is socket_server:
            indata = socket_server.recv(1024)
            if not indata:
                sockets.pop(1)
                socket_server.close()
            else:
                print(indata)