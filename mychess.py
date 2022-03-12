from shell import ShellThread
from pprint import pprint
from gmpy import scan1, setbit
import chess
import chess.svg
import time
import os

TEMP_SVG_PATH = './images/temp.svg'

board = chess.Board()

def save_svg(board, url=TEMP_SVG_PATH):
    with open(TEMP_SVG_PATH, 'w') as f:
        f.write(chess.svg.board(board=board))


def try_move(board: chess.Board, move):
    try:
        board.push(board.parse_san(move))
        return True
    except:
        return False

def update():
    save_svg(board)

piece_values = list(range(0, 11))
piece_values[chess.PAWN] = 100
piece_values[chess.KNIGHT] = 320
piece_values[chess.BISHOP] = 330
piece_values[chess.ROOK] = 500
piece_values[chess.QUEEN] = 900
piece_values[chess.KING] = 20000

pst = {}
pst[chess.PAWN] = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]
pst[chess.KNIGHT] = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]
pst[chess.BISHOP] = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]
pst[chess.ROOK] = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]
pst[chess.QUEEN] = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]
pst[chess.KING] = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

pst2 = {}
pst2[chess.WHITE] = {}
pst2[chess.BLACK] = {}
for piece, table in pst.items():
    pst2[chess.WHITE][piece] = [table[56 - (x // 8) * 16 + x] for x in range(0, 64)]
    pst2[chess.BLACK][piece] = table


def static_evaluation(board: chess.Board):
    evaluation = 0
    for color in chess.COLORS:
        multiplier = 1 if color == chess.WHITE else -1
        for piece_type in chess.PIECE_TYPES:
            bb = board.pieces_mask(piece_type, color)
            while bb != 0:
                square = scan1(bb)
                bb = setbit(bb, square, 0)
                value = piece_values[piece_type]
                evaluation += multiplier * (value + pst2[color][piece_type][square])
    return evaluation

result_values = {
    "1-0": float('inf'),
    "0-1": float('-inf'),
    "1/2-1/2": 0,
    "*": 0,
}

node_count = 0

def negamax_r(depth, alpha, beta):
    global node_count
    node_count += 1
    multiplier = 1 if board.turn == chess.WHITE else -1
    
    if depth == 0:
        return static_evaluation(board) * multiplier

    best = float('-inf')
    over = True
    for move in board.legal_moves:
        over = False
        board.push(move)
        best = max(best, -negamax_r(depth-1, -beta, -alpha))
        board.pop()
        alpha = max(alpha, best)
        if alpha >= beta:
            break

    if over:
        return result_values[board.result()]
    
    return best
    
def negamax(depth=3):
    global node_count
    start_time = time.time()
    start_nodes = node_count
    node_count += 1
    multiplier = 1 if board.turn == chess.WHITE else -1

    alpha = float('-inf')
    beta = float('+inf')
    
    if depth == 0:
        return static_evaluation(board) * multiplier

    best = (None, float('-inf'))
    over = True

    for move in board.legal_moves:
        over = False
        board.push(move)
        score = -negamax_r(depth-1, -beta, -alpha)
        if score > best[1]:
            best = (move, score)
        board.pop()
        alpha = max(alpha, best[1])
        if alpha >= beta:
            break
        print(move, score)

    if over:
        return result_values[board.result()]
    print('nodes:', node_count - start_nodes)
    print('nps:', (node_count - start_nodes) / (time.time() - start_time))
    return best[0]


# https://en.wikipedia.org/wiki/Principal_variation_search
def pvs():
    pass


def best_move(board: chess.Board):
    best = (None, float('-inf'))
    for move in board.legal_moves:
        board.push(move)
        evaluation = static_evaluation(board)
        if board.turn == chess.WHITE:
            evaluation *= -1
        if evaluation > best[1]:
            best = (move, evaluation)
        board.pop()
    return best[0]
    



if __name__ == "__main__":
    pass
    running = True
    while running:
        user_input = input('> ')
        if not try_move(board, user_input):
            print('invalid move :(')
            continue
        if board.is_game_over():
            print('You win! (or lose)')
            print(board.result())
            break
        move = negamax(3)
        print('      ' + str(move))
        board.push(move)
        print(board.promoted)
