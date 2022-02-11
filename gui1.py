import pygame
from solver import valid, solve
import time
pygame.init()

class Grid(object):
	board = [
		[7,8,0,4,0,0,1,2,0],
	    [6,0,0,0,7,5,0,0,9],
	    [0,0,0,6,0,1,0,7,8],
	    [0,0,7,0,4,0,2,6,0],
	    [0,0,1,0,5,0,9,3,0],
	    [9,0,4,0,6,0,0,0,5],
	    [0,7,0,3,0,0,0,1,2],
	    [1,2,0,0,0,7,4,0,0],
	    [0,4,9,2,0,6,0,0,7]
	]

	def __init__(self, row, col, width, height):
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(self.col)] for i in range(self.row)]
		self.selected = None
		self.model = None

	def update_model(self):
		self.model = [[self.cubes[i][j].value for j in range(self.col)] for i in range(self.row)]

	def place(self, val):
		row, col = self.selected
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set(val)
			self.update_model()

			if valid(self.model, val, (row, col)) and solve(self.model):
				return True

			else:
				self.cubes[row][col].set(0)
				self.cubes[row][col].set_temp(0)
				self.update_model()
				return False

	def draw(self, win):
		gap = self.width / 9
		for i in range(self.row + 1):
			thick = 4 if i % 3 == 0 and i != 0 else 1
			# row and col
			pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
			pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

		# draw cube
		for i in range(self.row):
			for j in range(self.col):
				self.cubes[i][j].draw()

	def sketch(self, val):
		row, col = self.selected
		self.cubes[row][col].set_temp(val)


	def select(self, row, col):
		#print(row, col)
		# resetting other
		for i in range(self.row):
			for j in range(self.col):
				self.cubes[i][j].selected = False

		self.cubes[row][col].selected = True
		self.selected = (row, col)

	def clear(self):
		row, col = self.selected
		if self.cubes[i][j].value == 0:
			self.cubes[i][j].set_temp(0)

	def click(self, pos):
		if pos[0] < self.width and pos[1] < self.height:
			gap = self.width // 9
			x = pos[0] // gap
			y = pos[1] // gap
			return(y, x)
		else:
			return None

	def is_finished(self):
		for i in range(self.row):
			for j in range(self.col):
				if self.cubes[i][j].value == 0:
					return False

		return True


class Cube(object):
	#row = 9
	#col = 9
	def __init__(self, value, row, col, width, height):
		self.value = value
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.selected = False
		self.temp = 0

	def draw(self):
		fnt = pygame.font.SysFont("comicsans", 40)
		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap

		if self.temp != 0 and self.value == 0:
			text1 = fnt.render(str(self.temp), 1, (128, 128, 128))
			win.blit(text1, (x + 5, y + 5))

		elif self.value != 0:
			text = fnt.render(str(self.value), 1, (0, 0, 0))
			win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_width() / 2)))

		if self.selected:
			pygame.draw.rect(win, (0, 0, 0), (x, y, gap, gap), 3)

	def set(self, val):
		self.value = val

	def  set_temp(self, val):
		self.temp = val


def redrawWindow(win, board, time, strike):
	win.fill((255, 255, 255))
	# draw time
	fnt = pygame.font.SysFont("comicsans", 40)
	text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
	win.blit(text, (540 - 160, 560))
	# draw strikes
	text = fnt.render("X " * strike, 1, (255, 0, 0))
	win.blit(text, (20, 560))
	# draw grid and boad
	board.draw(win)
	pygame.display.update()


def  format_time(secs):
	sec = secs % 60
	minute = secs // 60
	hour = minute // 60
	mat = " "+ str(minute) + ":" + str(sec)
	return mat

win = pygame.display.set_mode((540, 600))
pygame.display.set_caption("Sudoku")
board = Grid(9, 9, 540, 540)


# main loop
run = True
key = None
strike = 0
start = time.time()
while run:
	play_time = round(time.time() - start)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				key = 1
			if event.key == pygame.K_2:
				key = 2
			if event.key == pygame.K_3:
				key = 3
			if event.key == pygame.K_4:
				key = 4
			if event.key == pygame.K_5:
				key = 5
			if event.key == pygame.K_6:
				key = 6
			if event.key == pygame.K_7:
				key = 7
			if event.key == pygame.K_8:
				key = 8
			if event.key == pygame.K_9:
				key = 9
			if event.key == pygame.K_DELETE:
				board.clear()
				key = None

			if event.key == pygame.K_RETURN:
				i, j = board.selected
				if board.cubes[i][j].temp != 0:
					if board.place(board.cubes[i][j].temp):
						print("Success")
					else:
						print("Wrong")
						strike += 1
					key = None

					if board.is_finished():
						print("Game over!!!")
						sec = play_time % 60
						min = play_time // 60
						hour = min // 60
						print(f"Required time: {min} : {sec}")
						run = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			#print(pos)
			clicked = board.click(pos)
			if clicked:
				board.select(clicked[0], clicked[1])
				key = None

		if board.selected and key != None:
			board.sketch(key)


	redrawWindow(win, board, play_time, strike)

pygame.quit()
		