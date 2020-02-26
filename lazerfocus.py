import pygame

pygame.mixer.pre_init(44100,16,2,4096)

pygame.init()

screen = pygame.display.set_mode([1000, 900])
pygame.display.set_caption("Laser Focus")


def draw_piece(x, y, player, rotation):
	if player == 1:
		color = [250, 120, 120]
	else:
		color = [150, 150, 250]
	pygame.draw.rect(screen, color, ((115+100*x, 115+100*y), (70, 70)))
	pygame.draw.rect(screen, [0,0,0], ((115+100*x, 115+100*y), (70, 70)),3)
	if rotation == 0:
		pygame.draw.polygon(screen, [255,255,255], ((125+100*x, 120+100*y),(120+100*x, 125+100*y),(175+100*x, 180+100*y),(180+100*x, 175+100*y)))
		pygame.draw.polygon(screen, [0,0,0], ((125+100*x, 120+100*y),(120+100*x, 125+100*y),(175+100*x, 180+100*y),(180+100*x, 175+100*y)), 3)
	else:
		pygame.draw.polygon(screen, [255,255,255], ((175+100*x, 120+100*y),(180+100*x, 125+100*y),(125+100*x, 180+100*y),(120+100*x, 175+100*y)))
		pygame.draw.polygon(screen, [0,0,0], ((175+100*x, 120+100*y),(180+100*x, 125+100*y),(125+100*x, 180+100*y),(120+100*x, 175+100*y)), 3)

pieces = [[5,0,1,0],[6,0,1,0],[5,1,1,0],[6,1,1,0],[7,1,1,0],[5,2,1,0],[6,2,1,0],[7,2,1,0],   [5,6,2,1],[6,6,2,1],[5,5,2,1],[6,5,2,1],[7,5,2,1],[5,4,2,1],[6,4,2,1],[7,4,2,1]]

board = []
for x in range(1,7):
	board.append([x,0])
	board.append([x,6])
for x in range(1,8):
	board.append([x,1])
	board.append([x,3])
	board.append([x,5])
for x in range(0,8):
	board.append([x,2])
	board.append([x,4])

laser = []
def draw_laser():
	global laser
	laser = [0,3]
	direction = 0
	while laser[0]>-2 and laser[0]<9 and laser[1]>-2 and laser[1]<8 and not((laser == [7,0]) or (laser == [7,6])):
		lastlaser = laser
		if direction == 0:
			laser = [laser[0]+1,laser[1]]
		elif direction == 1:
			laser = [laser[0],laser[1]+1]
		elif direction == 2:
			laser = [laser[0]-1,laser[1]]
		elif direction == 3:
			laser = [laser[0],laser[1]-1]  
		pygame.draw.line(screen, [255,0,0], (150+100*lastlaser[0],150+100*lastlaser[1]), (150+100*laser[0],150+100*laser[1]), 6)
		for a in pieces:
			if laser[0] == a[0] and laser[1] == a[1]:
				if (a[3] == 0 and direction%2 == 0) or (a[3] == 1 and direction%2 ==1):
					direction = (direction+1)%4
				else:
					direction = (direction-1)%4
turn = 1
redwins = 0
bluewins = 0
def draw_screen():
	pygame.draw.rect(screen, [(250*redwins + 150*bluewins), (120*redwins + 150*bluewins), (120*redwins + 250*bluewins)], ((0, 0), (1000,900)))
	for x in range(0, 49):
		pygame.draw.rect(screen, [100*(2-x%2), 100*(2-x%2), 100*(2-x%2)], ((200+(x%7)*100, 100+int(x/7)*100), (100, 100)))

	pygame.draw.rect(screen, [100, 100, 100], ((100, 300), (100,100)))
	pygame.draw.rect(screen, [100, 100, 100], ((100, 500), (100,100)))
	pygame.draw.rect(screen, [100, 100, 100], ((815, 115), (70,70)), 3)
	pygame.draw.rect(screen, [100, 100, 100], ((815, 715), (70,70)), 3)
	for i in pieces:
		draw_piece(i[0],i[1],i[2],i[3])
	draw_laser()
	pygame.draw.rect(screen, [150, 150, 150], ((110, 410), (40,80)))
	pygame.draw.rect(screen, [140, 140, 140], ((150, 420), (40,60)))


draw_screen()
pygame.display.update()

def update_mouse():
	global mouse_pos
	global mouse_buttons
	pygame.event.pump()
	mouse_pos = pygame.mouse.get_pos()
	mouse_buttons = pygame.mouse.get_pressed()
	

play = True
while play:
	redwins = 0
	bluewins = 0
	update_mouse()
	selected = 0
	for i in pieces:
		if mouse_pos[0] > 115+100*i[0] and mouse_pos[0] < 185+100*i[0] and mouse_pos[1] > 115+100*i[1] and mouse_pos[1] < 185+100*i[1] and i[2] == turn:
			selected = i
			draw_screen()
			pygame.draw.rect(screen, [255,255,255], ((115+100*i[0], 115+100*i[1]), (70, 70)),3)
			pygame.display.update()
	if selected == 0:
		draw_screen()
		pygame.display.update()
	elif mouse_buttons[0]:
		pygame.time.delay(200)
		options = [[selected[0],selected[1]]]
		tempselected = selected
		while tempselected != 0:
			draw_screen()
			pygame.draw.rect(screen, [255,255,255], ((115+100*selected[0], 115+100*selected[1]), (70, 70)),3)
			for adjacent in [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]:
				occupied = 0
				for a in pieces:
					if selected[0]+adjacent[0] == a[0] and selected[1]+adjacent[1] == a[1]:
						occupied = 1
				if not [selected[0]+adjacent[0],selected[1]+adjacent[1]] in board:
					occupied = 1
				if not occupied:
					options.append([selected[0]+adjacent[0],selected[1]+adjacent[1]])
			for jumps in [[-2,-2],[2,-2],[-2,2],[2,2]]:
				occupied = 1
				for a in pieces:
					if selected[0]+(jumps[0]/2) == a[0] and selected[1]+(jumps[1]/2) == a[1] and selected[2] != a[2]:
						occupied = 0
				for a in pieces:
					if selected[0]+jumps[0] == a[0] and selected[1]+jumps[1] == a[1]:
						occupied = 1
				if not [selected[0]+jumps[0],selected[1]+jumps[1]] in board:
					occupied = 1
				if not occupied:
					options.append([selected[0]+jumps[0],selected[1]+jumps[1]])
			for a in options:
				pygame.draw.rect(screen, [255,255,255], ((115+100*(a[0]), 115+100*(a[1])), (70, 70)),3)
			pygame.display.update()
			tempselected = 0
			clicked = 0
		while clicked == 0:
			update_mouse()
			selectspace = 0
			for i in options:
				if mouse_pos[0] > 115+100*i[0] and mouse_pos[0] < 185+100*i[0] and mouse_pos[1] > 115+100*i[1] and mouse_pos[1] < 185+100*i[1]:
					selectspace = i
					draw_screen()
					for a in options:
							pygame.draw.rect(screen, [255,255,255], ((115+100*(a[0]), 115+100*(a[1])), (70, 70)),3)
					pygame.draw.rect(screen, [255,0,0], ((115+100*i[0], 115+100*i[1]), (70, 70)),3)
					pygame.display.update()
			if selectspace == 0:
				draw_screen()
				for a in options:
					pygame.draw.rect(screen, [255,255,255], ((115+100*(a[0]), 115+100*(a[1])), (70, 70)),3)
				pygame.display.update()
			if mouse_buttons[0]:
				pygame.time.delay(200)
				clicked = 1
		
		if selectspace != 0:
			turn = 3 - turn
			if selectspace[0] == selected[0] and selectspace[1] == selected[1]:
				for a in range(len(pieces)):
					if pieces[a][0] == selected[0] and pieces[a][1] == selected[1]:
						pieces[a][3] = 1 - pieces[a][3]
			if abs(selectspace[0]-selected[0]) == 2:
				for a in pieces:
				   if (selectspace[0] + selected[0])/2 == a[0] and (selectspace[1] + selected[1])/2 == a[1]:
					   pieces.remove(a)
			for a in range(len(pieces)):
				if pieces[a][0] == selected[0] and pieces[a][1] == selected[1]:
					pieces[a][0] = selectspace[0]
					pieces[a][1] = selectspace[1]
		draw_screen()
		pygame.display.update()
		
		redwins = 1
		bluewins = 1
		for a in pieces:
			if a[2] == 1:
				bluewins = 0
		for a in pieces:
			if a[2] == 2:
				redwins = 0
		if laser == [7,0]:
			redwins = 1
		if laser == [7,6]:
			bluewins = 1
		if bluewins or redwins:
			restart = 0
			draw_screen()
			pygame.display.update()
			while restart == 0:
				update_mouse()
				restart = mouse_buttons[0]
			pieces = [[5,0,1,0],[6,0,1,0],[5,1,1,0],[6,1,1,0],[7,1,1,0],[5,2,1,0],[6,2,1,0],[7,2,1,0],   [5,6,2,1],[6,6,2,1],[5,5,2,1],[6,5,2,1],[7,5,2,1],[5,4,2,1],[6,4,2,1],[7,4,2,1]]
			turn = 1
			draw_screen()
			pygame.display.update()
