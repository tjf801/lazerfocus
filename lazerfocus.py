import pygame
pygame.init()

K = 0.75
screen = pygame.display.set_mode((int(1000*K), int(900*K)))
pygame.display.set_caption("Laser Focus")

class Piece:
	def __init__(self, x, y, player, rotation):
		#TODO: remove all piece.x and piece.y in rendering, only use pixelx and pixely
		self.x = x
		self.y = y
		self.player = player
		self.color = (250, 120, 120) if player==1 else (150, 150, 250)
		self.rotation = rotation # 0 is \ (LEFT) and 1 is / (RIGHT)
		self.pixelx = (115+100*x)*K
		self.pixely = (115+100*y)*K
		#TODO: fully implement size
		self.size = 70*K
	
	#TODO: add a setcoords function, and have coordinates be internally stored as a tuple
	
	def __str__(self):
		return "player " + str(self.player) + " piece object at x=" + str(self.x) + " and y=" + str(self.y)
	
	def draw(self):
		self.pixelx = (115+100*self.x)*K
		self.pixely = (115+100*self.y)*K
		# draw the square
		pygame.draw.rect(screen, self.color, ((self.pixelx, self.pixely), (self.size, self.size)))
		# draw the border
		self.draw_border((0, 0, 0))
		#draw the mirror
		if self.rotation=="LEFT":
			pygame.draw.polygon(screen, [255,255,255], ((self.pixelx+10*K, self.pixely+5*K),(self.pixelx+5*K, self.pixely+10*K),(self.pixelx+60*K, self.pixely+65*K),(self.pixelx+65*K, self.pixely+60*K)))
			pygame.draw.polygon(screen, [0,0,0], ((self.pixelx+10*K, self.pixely+5*K),(self.pixelx+5*K, self.pixely+10*K),(self.pixelx+60*K, self.pixely+65*K),(self.pixelx+65*K, self.pixely+60*K)), int(3*K))
		else:
			pygame.draw.polygon(screen, [255,255,255], ((self.pixelx+60*K, self.pixely+5*K),(self.pixelx+65*K, self.pixely+10*K),(self.pixelx+10*K, self.pixely+65*K),(self.pixelx+5*K, self.pixely+60*K)))
			pygame.draw.polygon(screen, [0,0,0], ((self.pixelx+60*K, self.pixely+5*K),(self.pixelx+65*K, self.pixely+10*K),(self.pixelx+10*K, self.pixely+65*K),(self.pixelx+5*K, self.pixely+60*K)),int(3*K))
	
	def draw_border(self, color):
		self.pixelx = (115+100*self.x)*K
		self.pixely = (115+100*self.y)*K
		pygame.draw.rect(screen, color, ((self.pixelx, self.pixely), (self.size, self.size)), int(3*K))

class Board:
	def __init__(self):
		self.pieces = []
		for x in range(5, 8):
			for y in range(0, 3):
				if x!=7 or y!=0: self.pieces.append(Piece(x, y, 1, "LEFT"))
		for x in range(5, 8):
			for y in range(4, 7):
				if x!=7 or y!=6: self.pieces.append(Piece(x, y, 2, "RIGHT"))
		
		self.validspaces = [
					(1,0),	(2,0),	(3,0),	(4,0),	(5,0),	(6,0),	
					(1,1),	(2,1),	(3,1),	(4,1),	(5,1),	(6,1),	(7,1),#   blub blub im a fish
			(0,2),	(1,2),	(2,2),	(3,2),	(4,2),	(5,2),	(6,2),	(7,2),#    o
					(1,3),	(2,3),	(3,3),	(4,3),	(5,3),	(6,3),	(7,3),#   o
			(0,4),	(1,4),	(2,4),	(3,4),	(4,4),	(5,4),	(6,4),	(7,4),# o
					(1,5),	(2,5),	(3,5),	(4,5),	(5,5),	(6,5),	(7,5),#
					(1,6),	(2,6),	(3,6),	(4,6),	(5,6),	(6,6)
			]
	
	def __getitem__(self, addresses):
		x = addresses[0]
		y = addresses[1]
		for piece in self.pieces:
			if piece.x==x and piece.y==y:
				return piece
		return None
	
	def draw(self):
		for x in range(0, 49):
			pygame.draw.rect(screen, [100*(2-x%2), 100*(2-x%2), 100*(2-x%2)], (((200+(x%7)*100)*K, (100+int(x/7)*100)*K), (100*K, 100*K)))
		
		pygame.draw.rect(screen, [100, 100, 100], ((100*K, 300*K), (100*K,100*K)))
		pygame.draw.rect(screen, [100, 100, 100], ((100*K, 500*K), (100*K,100*K)))
		pygame.draw.rect(screen, [100, 100, 100], ((815*K, 115*K), (70*K,70*K)), int(3*K))
		pygame.draw.rect(screen, [100, 100, 100], ((815*K, 715*K), (70*K,70*K)), int(3*K))
	
	def get_move_options(self, piece):
		options = []
		
		x, y = piece.x, piece.y
		
		options.append((x, y))
		
		for a,b in [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]:
			if (self[x+a,y+b] is None) and ((x+a,y+b) in self.validspaces):
				options.append((x+a, y+b))
		
		for a,b in [(2,2), (2,-2), (-2,-2), (-2,2)]:
			if (self[x+a,y+b] is None) and ((self[x+(a//2),y+(b//2)] is not None) and self[x+(a//2),y+(b//2)].player!=piece.player) and ((x+a,y+b) in self.validspaces):
				options.append((x+a,y+b))
		
		return options

class Lazer:
	def __init__(self):
		pass
	
	def draw(self, board):
		self.x = 0
		self.y = 3
		self.direction = 0 # 0=+X; 1=+Y; 2=-X; 3=-Y;
		while (self.x > -2 and self.x < 9) and (self.y > -2 and self.y < 8) and not (self.x==7 and self.y in [0, 6]):
			lastx = self.x
			lasty = self.y
			
			if self.direction==0:
				self.x+=1
			elif self.direction==1:
				self.y+=1
			elif self.direction==2:
				self.x-=1
			elif self.direction==3:
				self.y-=1
			
			
			pygame.draw.line(screen, [255,0,0], ((150+100*lastx)*K,(150+100*lasty)*K), ((150+100*self.x)*K,(150+100*self.y)*K), 6)
			
			for piece in board.pieces:
				if self.x==piece.x and self.y==piece.y:
					if (piece.rotation=="LEFT" and self.direction in [0, 2]) or (piece.rotation=="RIGHT" and self.direction in [1, 3]):
						self.direction = (self.direction+1)%4
					else:
						self.direction = (self.direction-1)%4
		
		pygame.draw.rect(screen, [150, 150, 150], ((110*K, 410*K), (40*K,80*K)))
		pygame.draw.rect(screen, [140, 140, 140], ((150*K, 420*K), (40*K,60*K)))

board = Board()
lazer = Lazer()

def draw_screen():
	#draws the screen (duh)
	screen.fill((0, 0, 0))
	board.draw()
	for piece in board.pieces: piece.draw()
	lazer.draw(board)

def update():
	#updates pygames event queue
	#DO NOT FORGET TO CALL THIS OR PYGAME WILL CRASH
	for event in pygame.event.get(pump=True):
		if event.type==pygame.QUIT:
			pygame.quit()
			exit()

def get_mouse():
	#gets the mouse coordinates and buttons.
	mouse_pos = pygame.mouse.get_pos()
	mouse_buttons = pygame.mouse.get_pressed()
	return mouse_pos, mouse_buttons

def hover_over_piece():
	#highlights a piece if you hover over it
	selected = None
	selectedaddress = None
	for i, piece in enumerate(board.pieces):
		if mouse_pos[0] > (115+100*piece.x)*K and mouse_pos[0] < (185+100*piece.x)*K and mouse_pos[1] > (115+100*piece.y)*K and mouse_pos[1] < (185+100*piece.y)*K and piece.player == turn:
			selected = piece
			selectedaddress = i
			piece.draw_border((255, 255, 255))
	return selected, selectedaddress

def draw_options(options):
	#draws the list of options on screen
	for coord in options:
		pygame.draw.rect(screen, [255,255,255], (((115+100*(coord[0]))*K, (115+100*(coord[1]))*K), (70*K, 70*K)), int(3*K))

clock = pygame.time.Clock()
turn = 1
playing = True

draw_screen()
pygame.display.update()

while playing:
	update()
	mouse_pos, mouse_buttons = get_mouse()
	
	draw_screen()
	
	selected, selectedaddress = hover_over_piece()
	pygame.display.update()
	
	if mouse_buttons[0]:
		pygame.time.delay(200)
		if selected is not None:
			options = board.get_move_options(selected)
			
			draw_screen()
			selected.draw_border((255, 255, 255))
			draw_options(options)
			pygame.display.update()
			
			#waits for player to click on an option, or click off of the selected piece.
			clicked = False
			while not clicked:
				update()
				mouse_pos, mouse_buttons = get_mouse()
				
				selectedspace = None
				for option in options:
					if mouse_pos[0] > (115+100*option[0])*K and mouse_pos[0] < (185+100*option[0])*K and mouse_pos[1] > (115+100*option[1])*K and mouse_pos[1] < (185+100*option[1])*K:
						selectedspace = option
						draw_screen()
						draw_options(options)
						#draws a red box if you are hovering over an option
						pygame.draw.rect(screen, [255,0,0], (((115+100*option[0])*K, (115+100*option[1])*K), (70*K,70*K)), int(3*K))
						pygame.display.update()
				
				if selectedspace is None:
					draw_screen()
					draw_options(options)
					pygame.display.update()
				
				if mouse_buttons[0]:
					pygame.time.delay(200)
					clicked = True
			
			if selectedspace is not None:
				#if we are here, the player successfully chose a piece and moved it
				turn = 3 - turn
				
				if selectedspace==(selected.x, selected.y):
					#if we are here, the player chose to rotate the piece
					if selected.rotation=="LEFT":
						selected.rotation="RIGHT"
					elif selected.rotation=="RIGHT":
						selected.rotation="LEFT"
				elif abs(selectedspace[0]-selected.x)==2:
					#if we are here, the player chose to jump over a different piece
					for piece in board.pieces:
						if piece.x==(selectedspace[0]+selected.x)/2 and piece.y==(selectedspace[1]+selected.y)/2:
							board.pieces.remove(piece)
							break
				
				selected.x, selected.y = selectedspace
		
		draw_screen()
		pygame.display.update()
	
	
	#game end logic
	bluewins, redwins = True, True
	for piece in board.pieces:
		if piece.player == 1:
			bluewins = False
	for piece in board.pieces:
		if piece.player == 2:
			redwins = False
	if lazer.x==7 and lazer.y==0:
		redwins = True
	if lazer.x==7 and lazer.y == 6:
		bluewins = True
	if bluewins or redwins:
		#game is over
		pygame.time.delay(2000)
		screen.fill((0, 0, 0))
		pygame.display.update()
		restart = True
		while restart:
			update()
			mouse_pos, mouse_buttons = get_mouse()
			restart = not mouse_buttons[0]
		board = Board()
		turn = 1
		draw_screen()
		pygame.display.update()
pygame.quit()