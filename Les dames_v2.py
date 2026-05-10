id="damesclean"
import pygame

SIZE = 8
TILE = 80

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)

PLAYER_1 = 1
PLAYER_2 = 2
EMPTY = 0

pygame.init()
screen = pygame.display.set_mode((SIZE * TILE, SIZE * TILE))
pygame.display.set_caption("Jeu de Dames")

def create_board():
    board = []
    for y in range(SIZE):
        row = []
        for x in range(SIZE):
            if (x + y) % 2 == 0:
                row.append(GRAY)
            else:
                row.append(BLACK)
        board.append(row)
    return board


def create_pieces():
    pieces = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

    for y in range(3):
        for x in range(SIZE):
            if (x + y) % 2 != 0:
                pieces[y][x] = PLAYER_2

    for y in range(5, 8):
        for x in range(SIZE):
            if (x + y) % 2 != 0:
                pieces[y][x] = PLAYER_1

    return pieces

def draw(board, pieces, selected=None):
    for y in range(SIZE):
        for x in range(SIZE):
            pygame.draw.rect(screen, board[y][x], (x*TILE, y*TILE, TILE, TILE))

            if pieces[y][x] == PLAYER_1:
                pygame.draw.circle(screen, RED, (x*TILE+40, y*TILE+40), 30)
            elif pieces[y][x] == PLAYER_2:
                pygame.draw.circle(screen, BLUE, (x*TILE+40, y*TILE+40), 30)

    if selected:
        y, x = selected
        pygame.draw.rect(screen, YELLOW, (x*TILE, y*TILE, TILE, TILE), 3)

    pygame.display.flip()

def get_valid_moves(pieces, y, x, player):
    moves = []
    directions = []

    if player == PLAYER_1:
        directions = [(-1, -1), (-1, 1)]
    else:
        directions = [(1, -1), (1, 1)]

    for dy, dx in directions:
        ny, nx = y + dy, x + dx

        if 0 <= ny < SIZE and 0 <= nx < SIZE:
            if pieces[ny][nx] == EMPTY:
                moves.append((ny, nx))

            # capture
            if pieces[ny][nx] != EMPTY and pieces[ny][nx] != player:
                ny2, nx2 = ny + dy, nx + dx
                if 0 <= ny2 < SIZE and 0 <= nx2 < SIZE:
                    if pieces[ny2][nx2] == EMPTY:
                        moves.append((ny2, nx2))

    return moves


def move_piece(pieces, sy, sx, dy, dx, player):
    # capture
    if abs(dy - sy) == 2:
        my = (sy + dy) // 2
        mx = (sx + dx) // 2
        pieces[my][mx] = EMPTY

    pieces[dy][dx] = player
    pieces[sy][sx] = EMPTY



import random

def get_all_moves(pieces, player):
    all_moves = []

    for y in range(SIZE):
        for x in range(SIZE):
            if pieces[y][x] == player:
                moves = get_valid_moves(pieces, y, x, player)
                for move in moves:
                    all_moves.append((y, x, move[0], move[1]))

    return all_moves


def is_capture(move):
    sy, sx, dy, dx = move
    return abs(dy - sy) == 2


def ai_play(pieces, player):
    moves = get_all_moves(pieces, player)

    # prioriza capturas
    capture_moves = [m for m in moves if is_capture(m)]

    if capture_moves:
        move = random.choice(capture_moves)
    else:
        move = random.choice(moves)

    sy, sx, dy, dx = move
    move_piece(pieces, sy, sx, dy, dx, player)


def game():
    board = create_board()
    pieces = create_pieces()

    selected = None
    turn = PLAYER_1

    running = True
    while running:
        draw(board, pieces, selected)

        if turn == PLAYER_2:
            pygame.time.delay(500)
            ai_play(pieces, PLAYER_2)
            turn = PLAYER_1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER_1:
                x = event.pos[0] // TILE
                y = event.pos[1] // TILE

                if selected is None:
                    if pieces[y][x] == PLAYER_1:
                        selected = (y, x)
                else:
                    sy, sx = selected
                    valid_moves = get_valid_moves(pieces, sy, sx, PLAYER_1)

                    if (y, x) in valid_moves:
                        move_piece(pieces, sy, sx, y, x, PLAYER_1)
                        turn = PLAYER_2

                    selected = None

    pygame.quit()


game()
