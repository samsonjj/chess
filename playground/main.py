from shell import ShellThread
import cairosvg
import pygame
import queue
import threading
import mychess
import chess.svg
import random
import webbrowser
import os

TEMP_PNG_PATH = './images/temp.png'
TEMP_SVG_PATH = './images/temp.svg'
WIDTH, HEIGHT = (512, 512)

msg_queue = queue.Queue()

shared = {
    "running": True,
    "queue": msg_queue
}

# def pygame_load_svg(url=TEMP_SVG_PATH):
#     cairosvg.svg2png(url=url, write_to=TEMP_PNG_PATH)
#     return pygame.image.load(TEMP_PNG_PATH)

def save_svg(board, url=TEMP_SVG_PATH):
    with open(TEMP_SVG_PATH, 'w') as f:
        f.write(mychess.svg.board(board=board))

# webbrowser.open('file://' + os.path.realpath('index.html'))

# screen = pygame.display.set_mode((WIDTH, HEIGHT))

# shell_thread = ShellThread(shared)
# shell_thread.start()

# board = chess.Board()
# save_svg(board)

# # init screen
# image = pygame_load_svg(TEMP_SVG_PATH)
# screen.blit(image, (0,0))
# pygame.display.flip()

def try_move(board: mychess.Board, move):
    try:
        board.push(board.parse_san(move))
        return True
    except:
        return False

def update_chess_image(screen, board):
    save_svg(board)
    image = pygame_load_svg()
    screen.fill((0,0,0))
    screen.blit(image, (0,0))
    pygame.display.flip()

def handle_pygame_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shared["running"] = False

clock = pygame.time.Clock()
while shared["running"]:
    clock.tick(15)
    handle_pygame_events()
    if not msg_queue.empty():
        if not try_move(board, msg_queue.get()):
            print('invalid move :(')
            continue
        update_chess_image(screen, board)
    else:
        continue
    if board.is_game_over():
        print('You win! (or lose)')
    move = random.choice(list(board.legal_moves))
    print('->' + str(move))
    board.push(move)
    update_chess_image(screen, board)

                
pygame.quit()
pygame.display.quit()