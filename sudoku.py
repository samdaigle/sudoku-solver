
board = [
        [0, 0, 1, 3, 0, 2, 0, 0, 0],
        [0, 0, 3, 0, 0, 7, 0, 4, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 9],
        [0, 0, 6, 5, 0, 0, 0, 7, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 9, 0, 0, 0, 1, 4, 0, 0],
        [5, 0, 0, 0, 0, 0, 9, 0, 0],
        [6, 1, 0, 2, 0, 0, 8, 0, 0],
        [0, 0, 0, 9, 0, 8, 5, 0, 0]
]


def print_board(board):
    print("\n")
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print('| ', end="")
            if j == 8:
                print(board[i][j], end="\n")
            else:
                print(board[i][j], end=" ")
    print("\n")


def get_empty_space(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return (None, None)


def solve_board(board):
    row, col = get_empty_space(board)
    if row is None:
        return True

    for num in range(1, 10):
        if check_valid_number(board, num, (row, col)):
            board[row][col] = num

            if solve_board(board):
                return True

        board[row][col] = 0
    return False


def check_valid_number(board, number, pos):
    for i in range(len(board[0])):
        if board[pos[0]][i] == number and pos[1] != i:
            return False
    for i in range(len(board[0])):
        if board[i][pos[1]] == number and pos[0] != i:
            return False
    x = (pos[0] // 3) * 3
    y = (pos[1] // 3) * 3

    for i in range(x, x + 3):
        for j in range(y, y + 3):
            if board[i][j] == number and (i, j) != pos:
                return False
    return True


if __name__ == '__main__':
    solve_board(board)
    print_board(board)
