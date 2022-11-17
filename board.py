import random
from sudoku import check_valid_number, solve_board, print_board

board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def clear_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = 0


def new_board(board):

    clues = 27
    model = [[board[i][j]
              for j in range(len(board[0]))] for i in range(len(board))]
    used = []
    while clues > 0:
        for row in range(len(board)):
            count = 3
            while count > 0:
                col = random.randint(0, 8)
                num = random.randint(1, 9)
                if (row, col) in used:
                    continue
                if check_valid_number(model, num, (row, col)):
                    board[row][col] = num
                    model[row][col] = num
                    used.append((row, col))
                    count -= 1
                    clues -= 1
                else:
                    continue
    if solve_board(model):
        return True
    else:
        clear_board(board)
        new_board(board)


run = 0
yes = 0
no = 0
while run < 100:
    new_board(board)
    if solve_board(board):
        yes += 1
    else:
        no += 1
    clear_board(board)
    run += 1

print(f'yes = {yes}')
print(f'no = {no}')
