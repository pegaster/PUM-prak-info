import socket, sys, select, os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

socket_server = socket.socket()
server_host = socket.gethostname()
uid = ''
ip = socket.gethostbyname(server_host)
playerQuantity = 0
players = []
polutionx = 5
polutiony = 0
month = 0
gameStatus = 'connecting'
sport = 7777
polute_table = [(5, -20), (19, -8), (26, -3), (33, -3), (41, 7), (51, 14), (64, 21),
(80, 28), (100, 35), (110, 40), (121, 63), (133, 79), (146, 92), (161, 111), (177, 127)] # сделано руками
companiesNames = ['BASF', 'Dow', 'Sinopec', 'Sabic', 'Ineos', 'Formosa Plactic', 'ExxonMobil Chemical',
'LyondellBasell Industries', 'Mitsubishi Chemical', 'DuPont', 'LG Chem', 'Reliance Industries', 'PetroChina',
'Air Liquide', 'Toray Industries', 'Evonik Industries', 'Covestro', 'Bayer', 'Sumitomo Chemical', 'Braskem']
print('This is your IP address: ',ip)
companyNameIndex = 0
server_host = input('Enter server\'s IP address: ')

socket_server.connect((server_host, sport))
print('connection succesful...')
gameStatus = 'configuration'
sockets = [sys.stdin.fileno(), socket_server.fileno()]
while gameStatus != 'over':
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
                print(gameStatus)
                if gameStatus == 'configuration':
                    uid = indata[:36:].decode()
                    companyNameIndex = indata[36]
                    print(f'{companiesNames[companyNameIndex]} is your company name. Please wait start of the game')
                    gameStatus = 'connected'
                elif gameStatus == 'connected':
                    playerQuantity = indata[0]
                    if sys.platform == 'win32':
                        os.system('cls')
                    else:
                        os.system('clear')
                    print(f'Game started. Now month number {month} line postion is {polutionx}, line number is {polutiony}\nPlayer Table:')
                    for j in range(1, playerQuantity + 1):
                        if indata[j] == companyNameIndex:
                            print(f'{bcolors.FAIL}{companiesNames[indata[j]]} \t \t 0${bcolors().ENDC}')
                        else:
                            print(f'{companiesNames[indata[j]]} \t \t 0$')
                        players.append((indata[j], 0))
                        print('Please choose next month buisness strategy:')
                    gameStatus = 'in game'
                elif gameStatus == 'in game':
                    playerQuantity = indata[0]
                    if sys.platform == 'win32':
                        os.system('cls')
                    else:
                        os.system('clear')
                    if playerQuantity != 0:
                        month += 1
                        polutionx = indata[-2]
                        polutiony = indata[-1]
                        print(f'In game. Now month number {month} line postion is {polutionx}, line number is {polutiony}\nPlayer Table:')
                        for j in range(playerQuantity):
                            if indata[j * 4 + 1] == companyNameIndex:
                                print(f'{bcolors.FAIL}{companiesNames[indata[j * 4 + 1]]} \t \t {int.from_bytes(indata[j * 4 + 2 : j * 4 + 5], byteorder="big")}${bcolors.ENDC}')
                            else:
                                print(f'{companiesNames[indata[j * 4 + 1]]} \t \t {int.from_bytes(indata[j * 4 + 2 : j * 4 + 5], byteorder="big")}$')
                            players.append((indata[j], int.from_bytes(indata[j * 4 + 2 : j * 4 + 5], byteorder="big")))
                        print('Please choose next month buisness strategy:')
                    else:
                        print(f'{companiesNames[indata[1]]} win')
                        gameStatus = 'over'
                    
                #print(f'server: {indata}')
input('Press enter...')



