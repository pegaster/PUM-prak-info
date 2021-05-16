# Степан Днепров 2021 год для Предуниверсария МАИ
''' Весь мой код по практической работе размещен на моем github, он находится в свободном доступе, за людей скопировавших этот код отвественности не несу,
		при необходимости готов объяснить код лично, в целях доказательства подленности.
		Если же вы человек, который решил списать подчистую, это ваше право, я вас не заставлял'''
import socket # нужно для того, чтобы были сокеты
import sys # нужно, чтобы был сокет sys.stdin и для определения ос, которое нужно для очистки экрана
import select # нужно чтобы делать мультиплексирование
import uuid # нужно для раздачи уникальных id пользователям, вообще конкретно в нашем случае это не является обязяательным, но я никогда не писал клиент-серверные приложения до этого и мне хочется сделать все как можно ближе к тому, как это делают взрослые дяди
import os  # нужно для очистки экрана это не обязательно, но так красивее
import random # нужно для паводка и для выбора имени компании, второе не обязательно, но я хочу, чтобы моя игра не была чистой механикой
import logging # нужно для логирования
if sys.platform == 'win32':
	import msvcrt

class Player: # да, я использую классы в питоне, как структуры в Си
	def __init__(self, addres, companyNameIndex, uid):
		self.msg = ''
		self.money = 0
		self.uid = uid
		self.cni = companyNameIndex
		self.companyName = companiesNames[companyNameIndex]
		companiesNames.pop(companyNameIndex)
		self.addres = addres

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

server = socket.socket()
mode = True # для тестирования на одном компе True, для работы локалке False
if mode:
	ip = '127.0.0.1'
os.system('> server.log') # очищает старый лог
logging.basicConfig(format='%(asctime)s %(message)s', filename='server.log', datefmt='%H:%M:%S', level=logging.INFO) # здесь я задаю формат сообщений лога, файл и тип всех сообщений для более подробной информации ознакомьтесь с документацией библиотеки logging
server.bind((ip, 7777))
server.listen(15)
playerQuantity = 0
print('Server launched. Waiting users...')
# в эту переменную я буду писать разные значения в зависимости от режима программы
gameStatus = 'connecting'
players = {}
polutors = [] # игроки выбравшие первую стратегию
inspectors = [] # игроки выбравшие четвертую стратегию
cleaners = [] # игроки выбравшие вторую стратегию
isSomebodyChooseFive = False # переменная равна True, если хоть кто-то выбрал пятую стратегию
needUpdateInfo = True
needSendInfo = False
if sys.platform == 'win32':
	sockets = [server]
else:
	sockets = [sys.stdin, server]
clients = []

polutiony = 0
polutionx = 5
polute_table = [(5, -20), (19, -8), (26, -3), (33, -3), (41, 7), (51, 14), (64, 21),
(80, 28), (100, 35), (110, 40), (121, 63), (133, 79), (146, 92), (161, 111), (177, 127)] # сделано руками
companiesNamesList = ['BASF', 'Dow', 'Sinopec', 'Sabic', 'Ineos', 'Formosa Plactic', 'ExxonMobil Chemical',
'LyondellBasell Industries', 'Mitsubishi Chemical', 'DuPont', 'LG Chem', 'Reliance Industries', 'PetroChina',
'Air Liquide', 'Toray Industries', 'Evonik Industries', 'Covestro', 'Bayer', 'Sumitomo Chemical', 'Braskem'] # это тоже сделано руками
companiesNames = {i: companiesNamesList[i] for i in range(len(companiesNamesList))} # такая хитрая конструкция нужна чтобы имена выдавались случайно, без повторений, с сохранением индекса, а потом их значения можно было смотреть
winner = -1
month = 0
bonus = 0


def connectPlayer():
	global playerQuantity
	global needUpdateInfo
	conn, addrs = server.accept()
	clients.append(conn)
	playerQuantity += 1
	cnindex = int(random.choice(list(companiesNames)))
	
	uid = uuid.uuid4() # генерируется случайный уникальный пользовательский идентификатор, это нужно для логирования и последующей отладки
	players[conn] = Player(addrs[0], cnindex, uid)
	conn.send(bytes(str(uid).encode()) + (cnindex).to_bytes(1, byteorder='big'))
	logging.info(f'CONNECTED UUID: {str(uid)}, IP: {addrs[0]}, COMPANY_NAME_INDEX: {cnindex}')
	needUpdateInfo = True

def writeInfo():
	global gameStatus
	global playerQuantity
	global bonus
	if sys.platform == 'win32':
		os.system('cls')
	else:
		os.system('clear')
	if gameStatus == 'connecting':
		if playerQuantity == 0:
			print(f'There is no players on server yet. Your ip addres is {ip}')
		else:
			print(f'There is(are) {playerQuantity} player(s) on server:')
			for i in clients:
				print(f'{players[i].companyName}\t\t{players[i].addres}')
			print(f'\nYour ip is {ip}.\nPress enter to start game')
	elif gameStatus == 'in game':
		print(f'Now is month number {month}.\nLine positon is {polutionx}, line number is {polutiony}, bonus is {bonus}\nPlayers table:')
		for i in clients:
			print(f'{players[i].companyName}\t\t{players[i].addres}\t\t{players[i].money}$')
	if gameStatus == 'ended':
		print(f'{companiesNamesList[winner]} win!\n\n')
		gameStatus = 'over'

def checkStepEnd(): # функция, которая проверяет все ли игроки выбрали стратегию в этом игровом месяце
	for i in clients:
		if players[i].msg == '':
			return False
	return True

def gameLogic():
	global gameStatus
	global needUpdateInfo
	global needSendInfo
	global month
	global polutionx
	global polutiony
	global winner
	global bonus
	if gameStatus == 'in game':
		if(month <= 39) and checkStepEnd():
			bonus = 0
			polutors = []
			inspectors = []
			cleaners = []
			isSomebodyChooseFive = False
			for i in clients:
				if players[i].msg == '1':
					polutors.append(i)
					players[i].money += polute_table[polutiony + 8][0]
				elif players[i].msg == '2':
					cleaners.append(i)
					players[i].money += polute_table[polutiony + 8][1]
				elif players[i].msg == '3':
					players[i].money += 8
				elif players[i].msg == '4':
					inspectors.append(i)
				elif players[i].msg == '5':
					players[i].money += 8
					isSomebodyChooseFive = True
				players[i].msg = ''
			if isSomebodyChooseFive:
				for i in cleaners:
					players[i].money += 10
			if len(inspectors) > 0:
				for i in polutors:
					players[i].money -= 20
				for i in inspectors:
					players[i].money -= 8 // len(inspectors)
			if len(polutors) > 3:
				if (polutionx == 1) and (polutiony > -8):
					polutionx = 8
					polutiony -= 1
				elif(polutiony > -8):
					polutionx -= 1
			month += 1
			needUpdateInfo = True
			needSendInfo = True
			if month % 11 == 0 and month != 0:
				bonus = random.randint(1, 12)
				polutionx += bonus
				while polutionx > 8:
					polutionx -= 8
					polutiony += 1
		elif month == 40:
			winner = players[clients[0]].cni
			money = players[clients[0]].money
			for i in clients:
				if money < players[i].money:
					winer = players[i].cni
					money = players[i].money
			gameStatus = 'ended'
			needSendInfo = True
			needUpdateInfo = True
def sendInfo():
	global winner
	global playerQuantity
	for i in clients:
		if gameStatus == 'in game':
			message = (playerQuantity).to_bytes(1, byteorder='big')
			for j in clients:
				message += ((players[j].cni).to_bytes(1, byteorder='big') + (players[j].money).to_bytes(3, byteorder='big', signed=True))
			i.send(message + (polutionx).to_bytes(1, byteorder='big') + (polutiony).to_bytes(1, byteorder='big', signed=True))
			logging.info(f'SENDT UUID: {players[i].uid}, IP: {players[i].addres}, COMPANY_NAME_INDEX: {players[i].cni}, MESSAGE_VALUE: {message  + (polutionx).to_bytes(1, byteorder="big") + (polutiony).to_bytes(1, byteorder="big", signed=True)}')
		elif gameStatus == 'ended':
			i.send((winner).to_bytes(2, byteorder='big'))

def startGame():
	global needUpdateInfo
	global gameStatus
	global playerQuantity
	sys.stdin.readline()
	gameStatus = 'start'
	
	message = (playerQuantity).to_bytes(1, byteorder='big')
	for j in clients:
		message += (players[j].cni).to_bytes(1, byteorder='big')
	for i in clients:
		i.send(message)
		logging.info(f'SENT UUID: {players[i].uid}, IP: {players[i].addres}, COMPANY_NAME_INDEX: {players[i].cni}, MESSAGE_VALUE: {message}')
	needUpdateInfo = True
	gameStatus = 'in game'

while gameStatus != 'over':
	ins, _, _ = select.select(sockets + clients, [], [], 0)
	if sys.platform == 'win32':
		if msvcrt.kbhit():
			startGame()
	for i in ins:
		if i is server:
			if gameStatus == 'connecting':
				connectPlayer()
		elif i == sys.stdin:
			if gameStatus == 'connecting' and playerQuantity > 0:
				startGame()
			elif gameStatus == 'connecting' and playerQuantity == 0:
				sys.stdin.readline()
		else:
			data = i.recv(4)
			if not data:
				playerQuantity -= 1
				needUpdateInfo = True
				logging.info(f'DISCONNECTED UUID: {players[i].uid}, IP: {players[i].addres}, COMPANY_NAME_INDEX: {players[i].cni}')	
				i.close()
				clients.remove(i)
				players.pop(i)
				if(gameStatus != 'connecting' and playerQuantity == 0):
					print('Not enought players')
					gameStatus = 'over'
					break
			else:
				players[i].msg = data.decode()[0]
				logging.info(f'RECIVED UUID: {players[i].uid}, IP: {players[i].addres}, COMPANY_NAME_INDEX: {players[i].cni}, MESSAGE_VALUE: {data.decode()[0]}')

	gameLogic()
	if needSendInfo:
		sendInfo()
		needSendInfo = False
	if needUpdateInfo:
		writeInfo()
		needUpdateInfo = False
	
for j in range(2, len(sockets)):
	sockets[j].close()
print(''' #####     #    #     # #######    ####### #     # ####### ######  
#     #   # #   ##   ## #          #     # #     # #       #     # 
#        #   #  # # # # #          #     # #     # #       #     # 
#  #### #     # #  #  # #####      #     # #     # #####   ######  
#     # ####### #     # #          #     #  #   #  #       #   #   
#     # #     # #     # #          #     #   # #   #       #    #  
 #####  #     # #     # #######    #######    #    ####### #     # ''')
server.close()
input('\n\nPress enter ')
if sys.platform == 'win32':
	os.system('cls')
else:
	os.system('clear')