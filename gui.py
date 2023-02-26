import pygame
from sudoku import solve_board, check_valid_number, get_empty_space

pygame.font.init()


class Board:
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    def __init__(self, rows, cols, height, width, win):
        self.rows = rows
        self.cols = cols
        self.height = height
        self.width = width
        self.squares = [[Square(Board.board[i][j], i, j, width, height)
                         for j in range(cols)] for i in range(rows)]
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.squares[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set(val)
            self.update_model()

            if check_valid_number(self.model, val, (row, col)) and solve_board(self.model):
                return True
            else:
                self.squares[row][col].set(0)
                self.squares[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.squares[row][col].set_temp(val)

    def draw(self, win):
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (169, 169, 169), (0, i*gap),
                             (self.width, i*gap), thick)

            pygame.draw.line(win, (169, 169, 169), (i * gap, 0),
                             (i * gap, self.height), thick)
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(win)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].selected = False

        self.squares[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True

    def solve_gui(self):
        self.update_model()
        find = get_empty_space(self.model)
        if find == (None, None):
            return True
        else:
            row, col = find
            for i in range(1, 10):
                if check_valid_number(self.model, i, (row, col)):
                    self.model[row][col] = i
                    self.squares[row][col].set(i)
                    self.squares[row][col].draw_change(self.win, True)
                    self.update_model()
                    pygame.display.update()

                    if self.solve_gui():
                        return True
                    self.model[row][col] = 0
                    self.squares[row][col].set(0)
                    self.squares[row][col].draw_change(self.win, False)
                    self.update_model()
                    pygame.display.update()

            return False


class Square:

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont('arial', 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (169, 169, 169))
            win.blit(text, (x+5, y+5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (211, 211, 211))
            win.blit(text, (x + (gap/2 - text.get_width()/2),
                     y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("arial", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (32, 33, 36), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (211, 211, 211))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2),
                 y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (60, 186, 84), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (219, 50, 54), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board):
    win.fill((32, 33, 36))
    board.draw(win)


def main():
    win = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("SUDOKU")
    board = Board(9, 9, 540, 540, win)
    key = None
    run = True
    strikes = 0

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
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
                if event.key == pygame.K_c:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.squares[i][j].temp != 0:
                        if board.place(board.squares[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False
                if event.key == pygame.K_SPACE:
                    board.solve_gui()
                    key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

            if board.selected and key != None:
                board.sketch(key)

            redraw_window(win, board)
            pygame.display.update()


if __name__ == '__main__':
    main()
