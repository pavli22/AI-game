import math
import random
import sys
import numpy as np
import pygame


class Agent:
    def __init__(self, name, depth):
        self.name = name
        self.depth = depth

    def get_move(self, board):
        return self.minimax(board, self.depth, -math.inf, math.inf, True)[0]

    def score_position(self, board, piece):
        score = 0
        # Score center column
        center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score horizontal
        for r in range(ROWS):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMNS - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # Score vertical
        for c in range(COLUMNS):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROWS - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        # Score diagonal
        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_window(self, window, piece):
        score = 0
        opponent_piece = 1
        if piece == 1:
            opponent_piece = 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_locations = [col for col in range(COLUMNS) if is_valid_location(board, col)]
        is_terminal = winning_move(board, 1) or winning_move(board, 2) or len(valid_locations) == 0
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, 2):
                    return (None, 100000000000000)
                elif winning_move(board, 1):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board, 2))

        if maximizing_player:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, 2)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, 1)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return column, value

class Agent_minmax:
    def __init__(self, name, depth):
        self.name = name
        self.depth = depth

    def get_move(self, board):
        return self.minimax(board, self.depth, True)[0]

    def score_position(self, board, piece):
        score = 0
        # Score center column
        center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score horizontal
        for r in range(ROWS):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMNS - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # Score vertical
        for c in range(COLUMNS):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROWS - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        # Score diagonal
        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_window(self, window, piece):
        score = 0
        opponent_piece = 1
        if piece == 1:
            opponent_piece = 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def minimax(self, board, depth, maximizing_player):
        valid_locations = [col for col in range(COLUMNS) if is_valid_location(board, col)]
        is_terminal = winning_move(board, 1) or winning_move(board, 2) or len(valid_locations) == 0
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, 2):
                    return None, 100000000000000
                elif winning_move(board, 1):
                    return None, -10000000000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, score_position(board, 2)

        if maximizing_player:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, 2)
                new_score = minimax(b_copy, depth - 1, False)[1]
                if new_score > value:
                    value = new_score
                    column = col

            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, 1)
                new_score = self.minimax(b_copy, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    column = col

            return column, value



ROWS = 6
COLUMNS = 7
board = np.zeros((ROWS, COLUMNS))
def drop_piece(board, row, col, piece):
    board[row][col] = piece
def is_valid_location(board, col):
    return board[ROWS-1][col] == 0
def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r


def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, (0, 0, 255), (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, (0, 0, 0),
                               (int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2)),
                               RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, (255, 255, 0), (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check diagonal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check diagonal locations for win
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True

    return False


def evaluate_window(window, piece):
    score = 0
    opponent_piece = 1
    if piece == 1:
        opponent_piece = 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score
def print_board(board):
    print(np.flip(board, 0))


def score_position(board, piece):
    score = 0
    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # Score diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def minimax(board, depth, maximizing_player):
    valid_locations = [col for col in range(COLUMNS) if is_valid_location(board, col)]
    is_terminal = winning_move(board, 1) or winning_move(board, 2) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 2):
                return None, 100000000000000
            elif winning_move(board, 1):
                return None, -10000000000000
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, score_position(board, 2)

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col

        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 1)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col

        return column, value



def get_computer_move(board):
    return minimax(board, 5, True)[0]


pygame.init()
SQUARESIZE = 100
width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

player = 1
agent = None
while agent is None:
    print("Choose an agent to play against:")
    print("1. MinMAx agent")
    print("2. Alpha-Beta pruning agent")
    choice = input("> ")
    if choice == "1":
        agent = Agent_minmax("min-max-agent", 5)
    elif choice == "2":
        depth = int(input("Enter Level for agent: "
                          "1-Easy "
                          "2-Medium "
                          "3-Hard "))
        if depth==1 :
            agent = Agent("Alpha-Beta", 1)
        if depth==2:
            agent = Agent("Alpha-Beta", 3)
        if depth==3:
            agent = Agent("Alpha-Beta", 6)

    else:
        print("Invalid choice. Please choose again.")

game_over = False
turn = random.randint(0, 1)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == player:
                # Computer's turn
                col = get_computer_move(board)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    print("Computer wins!")
                    game_over = True

                turn += 1
                turn = turn % 2

                print_board(board)
                draw_board(board)

    if turn != player and not game_over:
        # Agent's turn
        col = agent.get_move(board)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, 3 - player)

        if winning_move(board, 3 - player):
            print("{} wins!".format(agent.name))
            game_over = True

        turn += 1
        turn = turn % 2

        print_board(board)
        draw_board(board)

    if game_over:
        pygame.time.wait(3000)