import random

board = [
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0]
]

# generate random values in row
board[0] = random.sample(range(1, 10), 9)

# generate full board
def generate(board):
	solve(board)

	# generate rondom postion to initialize value 0
	for i in range(len(board)):
		positions = random.sample(range(0, 9), 5)
		for pos in positions:
			board[i][pos] = 0

	return board


def  solve(board):
	find = find_emptyspot(board)
	if not find:
		return True
	else:
		row, col = find
	#print(board)
	for i in range(9, 0, -1):
		if valid(board, i, (row, col)):
			board[row][col] = i
			#print(i)

			if solve(board):
				return True

			board[row][col]  = 0

	return False


def valid(board, num, pos):
	# chacking in row:
	for j in range(len(board[0])):
		if board[pos[0]][j] == num and pos[1] != j:
			return False

	# cheing in column:
	for i in range(len(board)):
		if pos[0] != i and board[i][pos[1]] == num:
			return False

	# chacking in square:
	box_x = pos[1] // 3 # column
	box_y = pos[0] // 3 # row

	for i in range(box_y*3, box_y*3 + 3):
		for j in range(box_x*3, box_x*3 + 3):
			if board[i][j] == num and (i, j)!= pos:
				return False

	return True

#print(board)
def print_board(board):
	for i in range(len(board)):
		if i % 3 == 0  and i != 0:
			print("- - - - - - - - - - - - - - -")
		for j in range(len(board[i])):
			if j % 3 == 0 and j != 0:
				print("|", end = " ")
			if j == 8:
				print(str(board[i][j]))
			else:
				print(str(board[i][j]) + " ", end = " ")


def find_emptyspot(board):
	
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 0:
				 return (i, j)

	return False

def run():
	solve(board)
	print_board(board)
	print("_______________________________________")
	generate(board)
	print_board(board)

if __name__ == "__main__":
	run()