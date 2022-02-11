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
board[0] = random.sample(range(1, 10), 9)

def rotate(l, n):
    return l[n:] + l[:n]

def generate(board):
    for i in range(len(board)):
        if i >= 1: 
            if i % 3 != 0:
                board[i] = rotate(board[i-1], 3)
            else:
                board[i] = rotate(board[i-1], 1)

generate(board)
for i in range(len(board)):
    for j in range(len(board[0])):
        if j == 8:
            print(board[i][j])
        else:
            print(board[i][j], end = " ")
        
