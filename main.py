from shell import ShellThread
import cairosvg
import pygame
import queue
import threading
import chess
import chess.svg

TEMP_PNG_PATH = './images/temp.png'
TEMP_SVG_PATH = './images/temp.svg'
WIDTH, HEIGHT = (512, 512)

msg_queue = queue.Queue()

shared = {
    "running": True,
    "queue": msg_queue
}

def pygame_load_svg(url=TEMP_SVG_PATH):
    cairosvg.svg2png(url=url, write_to=TEMP_PNG_PATH)
    return pygame.image.load(TEMP_PNG_PATH)

def save_svg(board, url=TEMP_SVG_PATH):
    with open(TEMP_SVG_PATH, 'w') as f:
        f.write(chess.svg.board(board=board))

screen = pygame.display.set_mode((WIDTH, HEIGHT))

shell_thread = ShellThread(shared)
shell_thread.start()

board = chess.Board()
save_svg(board)

# init screen
image = pygame_load_svg(TEMP_SVG_PATH)
screen.blit(image, (0,0))
pygame.display.flip()

def perform_move(board: chess.Board, move):
    try:
        board.push(board.parse_san(move))
    except:
        print('invalid move: (')

def update_chess_image(screen, board):
    save_svg(board)
    image = pygame_load_svg()
    screen.fill((0,0,0))
    screen.blit(image, (0,0))
    pygame.display.flip()


clock = pygame.time.Clock()
while shared["running"]:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shared["running"] = False
    while not msg_queue.empty():
        perform_move(board, msg_queue.get())
        update_chess_image(screen, board)
        if board.is_game_over():
            print('You win! (or lose)')
        
pygame.quit()
pygame.display.quit()