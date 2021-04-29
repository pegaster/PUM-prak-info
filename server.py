    # Степан Днепров 2021 год для Предуниверсария МАИ
''' Весь мой код по практической работе размещен на моем github, он находится в свободном доступе, за людей скопировавших этот код отвественности не несу,
		при необходимости готов объяснить код лично, в целях доказательства подленности. Если же вы человек, который решил списать подчистую, это ваше право, я вас не заставлял'''
import socket
import sys
import select
import os # нужно для очистки экрана

class tcolors: # я хочу сделать вывод частично цветным: новое подключение зеленым, отключение красным
		HEADER = '\033[95m' # для этого использую escape-последоваельности
		OKBLUE = '\033[94m'
		OKCYAN = '\033[96m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'

class player:
		def __init__(self, addres, id):
			self.msg = ''
			self.money = 0
			self.id = id
			self.addres = addres

server = socket.socket()
server.bind(('localhost', 7777))
server.listen(15)
playerQuantity = 0
print('Server launched. Waiting users...')
game_msgs_types =['1\n', '2\n', '3\n', '4\n']
gameStatus = 'connecting' # в эту переменную я буду писать разные значения в зависимости от режима программы
players = {}
sockets = [sys.stdin, server]
ins, _, _ = select.select(sockets, [], [], 0)
while gameStatus != 'over':
	for i in ins:
			if i is server:
				if gameStatus == 'connecting':
					conn, addrs = server.accept()
					playerQuantity += 1
					print(f'{tcolors.OKGREEN}{addrs} is connected. There {playerQuantity} player(s) on server. Press Enter to start.')
					players[con] = player(addrs, playerQuantity)
					con.send(connected)
				elif i is sys.stdin:
					if gameStatus == 'connecting':
						gameStatus = 'start'
						os.system("clear") # очищает экран терминала перед началом игры, для windows os.system("cls"), на *nix(macOs, Linux, freeBSD и тд.) как у меня
						for j in range(2, len(sockets)):
							j.send('0\n')
						gameStatus = 'in game'
				elif gameStatus == 'in game':
					gameStatus == 'paused'
					print('Do you want to quit game? y/n')
				elif gameStatus == 'paused':
					data = i.readline()
					if data == 'n':
						gameStatus = 'in game'
					elif data == 'y':
						break
				else:
					data = i.recv(4)
					if data == None:
						playerQuantity -= 1
						print(f'{tcolor.WARNING}{addrs[i]} disconnected', end=' ')
						if(gameStatus != 'connecting' and playerQuantity == 0):
							print(f'{tcolor.WARNING}no players on server')
							print('Game Over')
							gameStatus = 'over'
							break
						
						else:
							print(f'{tcolor.WARNING}{len(msgs) - 1} players on server left')

						players.pop(i)
					elif data in game_msgs_types:
						players[i].msg = data


print('Game quited')
