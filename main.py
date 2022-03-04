import shutil
import pygame
import os 
from pygame.locals import *
import tkinter
import tkinter.filedialog
from shutil import copyfile
import random

pygame.init() 
pygame.font.init()

width = 525 # 100 per X/O and then 25 spacing between
height = 525
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

current_path = os.path.dirname(__file__) 
assets_path = os.path.join(current_path, 'assets')
data_path = os.path.join(current_path, 'data')

titleFont = pygame.font.SysFont('Calibri Light', 65)
subFont = pygame.font.SysFont('Calibri Light', 45)
genFont = pygame.font.SysFont('Calibri Light', 30)

def gameScreen(playersSelected, board=None, difficulty=None): # Diff 0 = Easy; 1 = Med; 2 = Hard
	print(playersSelected)
	if playersSelected == None or playersSelected[1] == None: return playerScreen(True)
	
	if playersSelected[0] == 10 or playersSelected[1] == 10: 
		computerPlaying = True
		if difficulty == None:
			difficulty = difficultyScreen(playersSelected)
	else: computerPlaying = False
	if playersSelected[0] == 10: # Hard coded nonsense, ensures the bot is always player2 
		playersSelected[0] = playersSelected[1]
		playersSelected[1] = 10

	if board == None: board =[["", "", ""],["", "", ""],["", "", ""]]
	playerData = loadPlayerData()
	player = 1

	if playerData[0][2] == "?": player1Symbol = pygame.image.load(os.path.join(assets_path, 'tick.png'))
	else: player1Symbol = pygame.image.load(os.path.join(assets_path, playerData[0][2]))
	
	if computerPlaying: 
		player2Symbol = pygame.image.load(os.path.join(assets_path, 'bot.png'))
	else: 
		if playerData[1][2] == "?": player2Symbol = pygame.image.load(os.path.join(assets_path, 'toe.png'))
		else: player2Symbol = pygame.image.load(os.path.join(assets_path, playerData[1][2]))
	
	
	# Resizes the images
	if player1Symbol.get_size()[0] > player1Symbol.get_size()[0]: player1Symbol = pygame.transform.scale(player1Symbol, (int((160/player1Symbol.get_size()[0])*player1Symbol.get_size()[1]), int((160/player1Symbol.get_size()[0])*player1Symbol.get_size()[1])))
	else: player1Symbol = pygame.transform.scale(player1Symbol, (int((160/player1Symbol.get_size()[1])*player1Symbol.get_size()[0]), int((160/player1Symbol.get_size()[1])*player1Symbol.get_size()[1])))
	
	if player2Symbol.get_size()[0] > player2Symbol.get_size()[0]: player2Symbol = pygame.transform.scale(player2Symbol, (int((160/player2Symbol.get_size()[0])*player2Symbol.get_size()[1]), int((160/player2Symbol.get_size()[0])*player2Symbol.get_size()[1])))
	else: player2Symbol = pygame.transform.scale(player2Symbol, (int((160/player2Symbol.get_size()[1])*player2Symbol.get_size()[0]), int((160/player2Symbol.get_size()[1])*player2Symbol.get_size()[1])))

	while True:
		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE: 
					return gamePausedScreen(board, playersSelected)
			if e.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				x = ""
				y = ""

				if pos[0] < 165: x = 0
				elif pos[0] > 173 and pos[0] < 353: x = 1
				elif pos[0] > 360: x = 2

				if pos[1] < 165: y = 0
				elif pos[1] > 173 and pos[1] < 353: y = 1
				elif pos[1] > 360: y = 2

				if x != "" and y != "": # If the position the mouse has clicked is not blank. i.e. an actual place has been pressed 
					if board[y][x] == "": # Ensure where they have placed is available 
						board[y][x] = player

						if checkWin(board, player): # If they have won 
							return endScreen(player, playersSelected)
						elif checkDraw(board): # If they have drawn 
							return endScreen("draw", playersSelected)
						else: # Rotate the players
							if computerPlaying: 
								compMove(board, difficulty)
								if checkWin(board, -1): 
									return endScreen(10, playersSelected)
								elif checkDraw(board): 
									return endScreen("draw", playersSelected)
							else: player *= -1

		row = 0
		col = 0
		screen.fill((255,255,255))
	
		row = 0 
		while row < len(board): 
			col = 0 
			while col < len(board[row]): 
				if board[row][col] == 1:
					screen.blit(player1Symbol, player1Symbol.get_rect(center=(80+col*180, 80+row*180)))
				elif board[row][col] == -1: 
					screen.blit(player2Symbol, player2Symbol.get_rect(center=(80+col*180, 80+row*180)))
					# screen.blit(player2Symbol, (5+col*167, 5+row*167))
				col += 1
			row += 1 

		#Draw after to prevent JPG white backgrou  nds being annoying
		pygame.draw.line(screen, (0,0,0), (165,0), (165,525), 8)#V1
		pygame.draw.line(screen, (0,0,0), (353,0), (353,525), 8)#V2
		pygame.draw.line(screen, (0,0,0), (0,165), (525,165), 8)#H1
		pygame.draw.line(screen, (0,0,0), (0,353), (525,353), 8)#H2

		pygame.display.update()
		clock.tick(30)
	
def difficultyScreen(playersSelected):
	difficultyButtons = []
	subTitlePlaceHolder = ""
	while True:
		screen.fill((0,0,0))
		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE: 
					return startScreen(playersSelected)
			elif e.type == pygame.MOUSEBUTTONDOWN:
				i = 0 
				while i < len(difficultyButtons):
					if difficultyButtons[i].collidepoint(pygame.mouse.get_pos()): 
						return i
					i += 1
			else:
				i = 0 
				while i < len(difficultyButtons):
					if difficultyButtons[i].collidepoint(pygame.mouse.get_pos()):
						print(pygame.mouse.get_pos())
						if i == 0: 
							subTitlePlaceHolder = "Like stealing candy from a baby."
						elif i == 1: 
							subTitlePlaceHolder = "Getting there.."
						elif i == 2:
							subTitlePlaceHolder =  "Good luck!"
					i += 1


		title = titleFont.render("Select your difficulty", True, (255, 0, 0))
		subtitle = genFont.render(subTitlePlaceHolder, False, (255, 0, 0))
		screen.blit(title, title.get_rect(center=(width//2, 50)))
		screen.blit(subtitle, subtitle.get_rect(center=(width//2, 85)))
		# pygame.draw.line(screen, (255,0,0), (width//5, 105), (width-(width//5), 105), 2)

		easyButton = subFont.render("Easy", True, (255, 0, 0))
		easyBtn = (screen.blit(easyButton, easyButton.get_rect(center=(width//2, 150))))
		medButton = subFont.render("Medium", True, (255, 0, 0))
		medBtn = (screen.blit(medButton, medButton.get_rect(center=(width//2, 200))))
		hardButton = subFont.render("Impossible", True, (255, 0, 0))
		hardBtn = (screen.blit(hardButton, hardButton.get_rect(center=(width//2, 250)))) 
		
		if len(difficultyButtons) < 3: 
			difficultyButtons.append(easyBtn)
			difficultyButtons.append(medBtn)
			difficultyButtons.append(hardBtn)
			

		pygame.display.update()
		clock.tick(30)

def startScreen(playersSelected=None):
	# playersSelected = [10, 1]
	startButtons = []
	while True:
		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					return gameScreen(playersSelected)
			if e.type == pygame.MOUSEBUTTONDOWN:
				i = 0 
				while i < len(startButtons):
					if startButtons[i].collidepoint(pygame.mouse.get_pos()): 
						if i == 0: return gameScreen(playersSelected)
						elif i == 1: return playerScreen(False, playersSelected)
					i += 1

		screen.fill((0,0,0))
		title = titleFont.render("TIC TAC TOE", True, (255, 0, 0))
		subtitle = subFont.render("press space to start!", False, (255, 0, 0))
		screen.blit(title, title.get_rect(center=(width//2, 50)))
		screen.blit(subtitle, subtitle.get_rect(center=(width//2, 85)))
		pygame.draw.line(screen, (255,0,0), (width//5, 105), (width-(width//5), 105), 2)
	
		playButton = subFont.render("Play Game", True, (255, 0, 0))
		startButtons.append(screen.blit(playButton, playButton.get_rect(center=(width//2, 150))))
		playerButton = subFont.render("Players", True, (255, 0, 0))
		startButtons.append(screen.blit(playerButton, playerButton.get_rect(center=(width//2, 200))))
		

		pygame.display.update()
		clock.tick(30)

def gamePausedScreen(board, playersSelected):
	while True: 
		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN: 
				if e.key == pygame.K_SPACE or e.key == pygame.K_ESCAPE:
					return gameScreen(playersSelected, board)
				elif e.key == pygame.K_END:
					return startScreen(playersSelected)
					
	
		screen.fill((255,255,255))
		title = titleFont.render("Game Paused", True, (0, 0, 0))
		subtitle = subFont.render("press space to resume", True, (255, 0, 0))
		screen.blit(title, title.get_rect(center=(width//2, height//2)))
		screen.blit(subtitle, subtitle.get_rect(center=(width//2, 25+height//2)))

		pygame.display.update()
		clock.tick(30)

def endScreen(winner, playersSelected):
	playerData = loadPlayerData()

	print(winner)
	if winner != 10 and winner != "draw": 
		playerData[winner][1] = str(int(playerData[winner][1]) + 1)
		savePlayerData(playerData)

	# Horrible, again, should've been changed in the other function
	if winner == 1: winner = 0
	elif winner == -1: winner = 1

	while True: 
		for e in pygame.event.get(): 
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					return gameScreen(playersSelected)
				elif e.key == pygame.K_ESCAPE:
					return startScreen(playersSelected)

		screen.fill((0,0,0))
		title = titleFont.render("Game Over!", True, (255, 0, 0))
		screen.blit(title, title.get_rect(center=(width//2, height//2)))

		if winner == "draw": subtitle = subFont.render("Both players have drawn...", True, (255, 0, 0))
		elif winner == 10: subtitle = subFont.render("The bot has won!", True, (255, 0, 0))
		else: subtitle = subFont.render(playerData[winner][0] + " has won!", True, (255, 0, 0))
		
		screen.blit(subtitle, subtitle.get_rect(center=(width//2, 40+height//2)))
		instructions = subFont.render("Escape for menu | Space to replay", True, (255, 0, 0))
		screen.blit(instructions, instructions.get_rect(center=(width//2, height-50)))

		pygame.display.update()
		clock.tick(30)



def playerScreen(promptSelection=False, playersSelected=None, promptSelectTwo=False):
	playerData = loadPlayerData()
	playerButtons = []

	while True:
		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN: 
				if e.key == pygame.K_ESCAPE or e.key == pygame.K_RETURN or e.key == K_SPACE: 
					return startScreen(playersSelected)
			if e.type == pygame.MOUSEBUTTONDOWN:
				print(pygame.mouse.get_pressed())
				if pygame.mouse.get_pressed() == (0, 0, 1): #RMB
					i = 0
					while i < len(playerButtons)-1:
						if playerButtons[i].collidepoint(pygame.mouse.get_pos()): 
							return playerSettings(i, playerData)
						i += 1
				elif pygame.mouse.get_pressed() == (1, 0, 0): # LMB
					i = 0
					while i < len(playerButtons):
						if playerButtons[i].collidepoint(pygame.mouse.get_pos()): 
							return playerSelect(i, playersSelected, promptSelection)
						i += 1
					
					
		screen.fill((0,0,0))
		if promptSelection or promptSelectTwo: 
			instructions = titleFont.render("Please select 2 players", True, (255, 0, 0))
			subtitle = subFont.render("Then press escape to return", False, (255, 0, 0))
		else:
			instructions = titleFont.render("Players Menu", True, (255, 0, 0))
			subtitle = subFont.render("Press escape to return", False, (255, 0, 0))
		screen.blit(instructions, instructions.get_rect(center=(width//2, 50)))
		screen.blit(subtitle, subtitle.get_rect(center=(width//2, 85)))

		x = 0
		while x < len(playerData)+1: 
			if x < len(playerData): 
				if playersSelected != None and (playersSelected[0] == x or playersSelected[1] == x): subtitle = genFont.render("#" + str(x+1) + " " + playerData[x][0] + " | Total Score = " + playerData[x][1], False, (255, 100, 100))
				else: subtitle = genFont.render("#" + str(x+1) + " " + playerData[x][0] + " | Total Score = " + playerData[x][1], False, (255, 0, 0))
				button = screen.blit(subtitle, subtitle.get_rect(center=(width//2, (x+1)*30+125)))
				if len(playerButtons) < 10: playerButtons.append(button)
			else: 
				if playersSelected != None and (playersSelected[0] == x or playersSelected[1] == x): subtitle = genFont.render("Computer AI", False, (255, 100, 100))
				else: subtitle = genFont.render("Computer AI", False, (255, 0, 0))
				button = screen.blit(subtitle, subtitle.get_rect(center=(width//2, (x+1)*30+125)))
				if len(playerButtons) < 11: playerButtons.append(button)
			x+=1
		

		
		pygame.display.update()
		clock.tick(30)

def playerSettings(playerNum, playerData): 
	takingInput = False
	userInput = ""
	fieldSelected = None

	while True:
		player = playerData[playerNum][0]
		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN:
				if takingInput:
					if e.unicode.isalpha():
						userInput += e.unicode
					elif e.key == K_BACKSPACE:
						userInput = userInput[:-1]
					elif e.key == K_RETURN or e.key == K_DOWN:
						takingInput = False
						if fieldSelected == "name": 
							if userInput != "": playerData[playerNum][0] = userInput
							fieldSelected = "imagePath"
						elif fieldSelected == "imagePath": 
							fieldSelected = "resetPlayer"
						if fieldSelected == "resetPlayer" and e.key == K_RETURN: 
							playerData[playerNum][0] = "Unknown" 
							playerData[playerNum][1] = "0"
							if (playerNum % 2) == 0: playerData[playerNum][2] = "tick.png"
							else: playerData[playerNum][2] = "toe.png"
						userInput = ""
					elif e.key == K_ESCAPE:
						takingInput = False 
						userInput = ""
						fieldSelected = None

				elif e.key == K_ESCAPE:
					savePlayerData(playerData)
					return playerScreen

				
				elif e.key == K_DOWN: 
					if fieldSelected == None: fieldSelected = "name"
					elif  fieldSelected == "name": fieldSelected = "imagePath"
					elif fieldSelected == "imagePath": fieldSelected = "resetPlayer"
					elif fieldSelected == "resetPlayer": fieldSelected = "name" 
					
					if fieldSelected != None: takingInput = True
				elif e.key == K_UP:
					if fieldSelected == None: fieldSelected = "resetPlayer"
					elif fieldSelected == "name": fieldSelected = "resetPlayer"
					elif fieldSelected == "imagePath": fieldSelected = "name"
					elif fieldSelected == "resetPlayer": fieldSelected = "imagePath"
					
					if fieldSelected != None: takingInput = True
				
				elif e.key == K_RETURN:
					if fieldSelected == "imagePath":
						return loadImage(playerNum, playerData)
				
		screen.fill((0,0,0))
		title = titleFont.render("Player Settings", True, (255, 0, 0))
		subtitle = subFont.render(player, True, (255, 0, 0))
		screen.blit(title, title.get_rect(center=(width//2, 50)))
		screen.blit(subtitle, subtitle.get_rect(center=(width//2, 85)))
		
		if fieldSelected == "name" and userInput != "": 
			nameField = genFont.render("Name: " + userInput , True, (255, 0, 0))
		else: 
			nameField = genFont.render("Name: " + playerData[playerNum][0], True, (255, 0, 0))

		imageField = genFont.render("Icon: " + playerData[playerNum][2], True, (255, 0, 0))
		resetField = genFont.render("Reset Player", True, (255, 0, 0))

		arrow = genFont.render("> ", True, (255, 0, 0))
		if fieldSelected == "name": screen.blit(arrow, (10, 117))
		elif fieldSelected == "imagePath": screen.blit(arrow, (10, 150))
		elif fieldSelected == "resetPlayer": screen.blit(arrow, (10, 180))
		screen.blit(nameField, (30, 120))
		screen.blit(imageField, (30, 150))
		screen.blit(resetField, (30, 180))

		pygame.display.update()
		clock.tick(30)

def playerSelect(playerNum, currentPlayers, promptedSelection=False): 
	if currentPlayers == None or currentPlayers[0] == None: currentPlayers = [playerNum, None]
	elif currentPlayers[0] == playerNum: # If the player trying to select is in index 0
		if currentPlayers[1] == None: currentPlayers = None
		else: currentPlayers = [currentPlayers[1], None]
	elif currentPlayers[1] == None: currentPlayers[1] = playerNum
	elif currentPlayers[0] == playerNum: currentPlayers = None
	elif (currentPlayers[0] != None and currentPlayers[1] != None): currentPlayers = [playerNum, None] # If both players selected, or no players selected
	else: # If the first player is selected, but the other is not
		currentPlayers[1] = playerNum
	
	if promptedSelection:
		if currentPlayers[1] != None: return gameScreen(currentPlayers)
		else: return playerScreen(True, currentPlayers, True)
	else: 
		if currentPlayers == None: return playerScreen(False, currentPlayers, False)
		elif currentPlayers[1] == None: return playerScreen(False, currentPlayers, True)
		else: return playerScreen(False, currentPlayers, False)

def loadPlayerData(): 
	playerData = []
	playerDataFile = open(os.path.join(data_path, "playerdata.txt"), "r")

	for line in playerDataFile.readlines(): 
		if(len(playerData) < 10): playerData.append(line.replace("\n", "").split("|"))

	return playerData 

def savePlayerData(playerData):
	playerDataFile = open(os.path.join(data_path, "playerdata.txt"), "w")

	data = ""
	p = 0 
	while p < len(playerData): 
		v = 0 
		while v < len(playerData[p]):
			data = data + playerData[p][v]
			if v != (len(playerData[p])-1): data = data + "|" 
			v += 1
		p += 1
		data = data + "\n"
	
	playerDataFile.write(data)

def loadImage(playerNum, playerData):
	playerData = loadPlayerData()

	top = tkinter.Tk()
	top.withdraw()  # hide window
	file = tkinter.filedialog.askopenfile(parent=top, filetypes=[("PNG", ".png"), ("JPG", "jpg")])
	shutil.copy(str(file.name), assets_path)
	
	top.destroy()

	playerData[playerNum][2] = str(file.name.split("/")[(len(file.name.split("/"))-1)])
	savePlayerData(playerData)

	return playerSettings(playerNum, playerData)

def checkWin(board, player):
	possibleWins = [[[0,0], [0,1], [0, 2]],[[1,0],[1, 1],[1,2]], [[1,0],[1, 1],[1,2]], [[2,0],[2, 1],[2,2]], [[0,0],[1, 0],[2,0]], [[0,1],[1, 1],[2,1]], [[0,2],[1, 2],[2,2]], [[0,0],[1, 1],[2,2]], [[0,2],[1, 1],[2,0]]]
	
	for route in possibleWins:
		if board[route[0][0]][route[0][1]] == player and board[route[1][0]][route[1][1]] == player and board[route[2][0]][route[2][1]] == player:
			return True
	return False 

def checkDraw(board):
	filled = True
	for row in board: 
		for place in row:
			if place == "": 
				filled = False
	return filled

def miniMax(board, isMaximizing):
	if checkWin(board, -1): return 100 #The bot has won 
	elif checkWin(board, 1): return -250 #The player has won
	elif checkDraw(board): return 0

	if isMaximizing: 
		bestScore = -800 

		row = 0 
		while row < 3: 
			col = 0 
			while col < 3:  
				if(board[row][col] == ""): 
					board[row][col] = -1   
					score = miniMax(board, False)
					board[row][col] = ""
					if score > bestScore: 
						bestScore = score 

				col += 1
			row += 1	
	else: # If not maximising 
		bestScore = 800 

		row = 0 
		while row < 3: 
			col = 0 
			while col < 3:  
				if(board[row][col] == ""): 
					board[row][col] = 1
					score = miniMax(board, True)
					board[row][col] = ""
					if score < bestScore: 
						bestScore = score 
				col += 1
			row += 1
	
	return bestScore

def compMove(board, difficulty): 
	bestScore = -800 
	bestMove = [0, 0]
	topMoves = []

	row = 0 
	while row < 3: 
		col = 0 
		while col < 3:  
			if(board[row][col] == ""): 
				board[row][col] = -1   
				score = miniMax(board, False)
				board[row][col] = ""
				if score > bestScore: 
					bestScore = score
					bestMove = [row,col]
					
				if score > (bestScore-500):
					topMoves.append([row,col])
					print(topMoves)

			col += 1
		row += 1	
	
	if difficulty == 2: board[bestMove[0]][bestMove[1]] = -1 # Always go for best move 
	else:
		chance = random.randint(0, 100)
		lastTopMovesIndex = len(topMoves)-1


		if difficulty == 1: 
			if chance < 50: # 50% chance of doing best move 
				board[bestMove[0]][bestMove[1]] = -1
			else: # 50% chance of doing second or third best move 
				if random.randint(1,2) == 1: board[topMoves[lastTopMovesIndex-1][0]][topMoves[lastTopMovesIndex-1][1]] = -1
				else: board[topMoves[lastTopMovesIndex-2][0]][topMoves[lastTopMovesIndex-2][1]] = -1
		
		else: # 25% chance of doing best move 
			if chance < 25: #Do the hardest 
				board[bestMove[0]][bestMove[1]] = -1
			else:
				if random.randint(1,2) == 1: board[topMoves[lastTopMovesIndex-1][0]][topMoves[lastTopMovesIndex-1][1]] = -1
				elif random.randint(1,2) == 1: board[topMoves[lastTopMovesIndex-2][0]][topMoves[lastTopMovesIndex-2][1]] = -1
				else: board[topMoves[lastTopMovesIndex-3][0]][topMoves[lastTopMovesIndex-3][1]] = -1




currentScreen = startScreen
exitGame = False 

while not exitGame:
	for e in pygame.event.get():
		if e.type == pygame.QUIT: 
			endProgram = True 

	currentScreen = currentScreen()
	print(currentScreen)
	if currentScreen == None: 
		exitGame = True 

	pygame.display.update()
	clock.tick(30)
		
pygame.quit()
quit()
