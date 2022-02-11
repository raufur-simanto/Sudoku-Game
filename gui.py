# Sudoku by using pygame
# created by Raufur Rahman

import pygame
from solver import valid, solve, generate, board
import time
import random
pygame.init()


class Grid():

	def __init__(self, row, col, width, height):
		self.board = generate(board)
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(self.col)] for i in range(self.row)]
		self.selected = None
		self.model = None
		

	def update_model(self):
		self.model = [[self.cubes[i][j].value for j in range(self.col)] for i in range(self.row)]

	def draw(self, win):
		gap = self.width / 9
		for i in range(self.row + 1):
			thick = 4 if i % 3 ==0 and i != 0 else 1
			# draw row
			pygame.draw.line(win, (0, 0, 0), (0, gap * i), (self.width, gap * i), thick)
			# draw col 
			pygame.draw.line(win, (0, 0, 0), (gap * i, 0), (gap * i, self.height), thick)

		# draw cube
		for i in range(self.row):
			for j in range(self.col):
				self.cubes[i][j].draw(win)

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

	def click(self, pos):
		if pos[0] < self.width and pos[1] < self.height:
			gap = self.width // 9
			x = pos[1] // gap
			y = pos[0] // gap
			return(x, y)
		else:
			return None

	def select(self, row, col):
		# reset all other
		for i in range(self.row):
			for j in range(self.col):
				self.cubes[i][j].selected = False
		
		self.cubes[row][col].selected = True
		self.selected = (row, col)

	def clear(self):
		row, col = self.selected
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set_temp(0)

	def sketch(self, val):
		row, col = self.selected
		self.cubes[row][col].set_temp(val)

	def is_finished(self, win):
		for i in range(self.row):
			for j in range(self.col):
				if self.cubes[i][j].value == 0:
					return True
		is_finish(win)
		time.sleep(3)
		return False


class Cube():
	def __init__(self, value, row, col, width, height):
		self.value = value
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.selected = False
		self.temp = 0

	def draw(self, win):
		fnt = pygame.font.SysFont("comicsans", 40)
		gap = self.width / 9
		x = gap * self.col 
		y = gap * self.row

		if self.temp != 0 and self.value == 0:
			text1 = fnt.render(str(self.temp), 1, (128, 128, 128))
			win.blit(text1, (x + 5, y + 5))

		elif self.value != 0:
			text = fnt.render(str(self.value), 1, (0, 0, 0))
			win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_width()/2)))
		
		if self.selected:
			pygame.draw.rect(win, (0, 0, 0), (x, y, gap, gap), 3)

	def set(self, val):
		self.value = val 

	def set_temp(self, val):
		self.temp = val


def  format_time(secs):
	sec = secs % 60
	minute = secs // 60
	hour = minute // 60
	if sec >= 10:
		mat = " "+ str(minute) + ":" + str(sec)
	else:
		mat = " "+str(minute) + ":0" + str(sec)

	return mat


def redrawWindow(win, board, time, strike):
	win.fill((255, 255, 255))
	# draw time
	fnt = pygame.font.SysFont("comicsans", 40)
	text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
	win.blit(text, (540 - 160, 560))
	# draw strikes
	text = fnt.render("X " * strike, 1, (255, 0, 0))
	win.blit(text, (20, 560))
	# draw grid and board
	board.draw(win)
	pygame.display.update()


def is_finish(win):
	fnt = pygame.font.SysFont("comicsans", 80)
	text = fnt.render("Finished!!!", 1, (255, 0, 0))
	win.blit(text, (80, 250))
	pygame.display.update()


def time_up(win):
	fnt = pygame.font.SysFont("comicsans", 80)
	text = fnt.render("Time's Up!!!", 1, (255, 0, 0))
	win.blit(text, (80, 250))
	pygame.display.update()
	

def high_penalty(win):
	fnt = pygame.font.SysFont("comicsans", 80)
	text = fnt.render("High Penalty!!!", 1, (255, 0, 0))
	win.blit(text, (80, 250))
	pygame.display.update()


# game loop
def main():
	# create game window
	win = pygame.display.set_mode((540,600))
	pygame.display.set_caption("Sudoku")
	# create Grid object
	board = Grid(9, 9, 540, 540)
	#board.board[0] = random.sample(range(1, 10), 9)
	#board.board = generate(board.board)
	run = True
	key = None
	strikes = 0
	time_limit = 13*60
	start = time.time()

	while run:
		play_time = round(time.time() - start)
		time_left = time_limit - play_time

		run = board.is_finished(win)
			
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
							#print("Success!!")
							pass
						else:
							#print("Wrong!!!")
							strikes += 1
						key = None

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				clicked = board.click(pos)
				if clicked:
					board.select(clicked[0], clicked[1])
					key = None

			if board.selected and key != None:
				board.sketch(key)

		if time_left >= 0:
			redrawWindow(win, board, time_left, strikes)

		# for high penalty
		if strikes >= 7:
			high_penalty(win)
			run = False
			time.sleep(3)
			main()

		# checking time
		if time_left < 0:
			time_up(win)
			run = False
			time.sleep(3)
			main()

main()
pygame.quit()


				

