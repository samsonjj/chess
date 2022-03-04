from shell import ShellThread
import mychess
import chess.svg
import webbrowser
import os
import random

TEMP_SVG_PATH = './images/temp.svg'

def save_svg(board, url=TEMP_SVG_PATH):
    with open(TEMP_SVG_PATH, 'w') as f:
        f.write(mychess.svg.board(board=board))


def try_move(board: mychess.Board, move):
    try:
        board.push(board.parse_san(move))
        return True
    except:
        return False

board = mychess.Board()
def update():
    save_svg(board)

piece_values = list(range(0, 11))
piece_values[mychess.PAWN] = 1
piece_values[mychess.KNIGHT] = 3
piece_values[mychess.BISHOP] = 3
piece_values[mychess.ROOK] = 5
piece_values[mychess.QUEEN] = 9
piece_values[mychess.KING] = 10

def static_evaluation(board):
    evaluation = 0
    for square, piece in board.piece_map().items():
        multiplier = 1 if piece.color == mychess.WHITE else -1

        value = piece_values[piece.piece_type]
        evaluation += multiplier * value
        if piece.piece_type == mychess.PAWN and square in [mychess.D5, mychess. D4, mychess.E4, mychess.E5]:
            evaluation += multiplier * .1
    return evaluation

result_values = {
    "1-0": float('inf'),
    "0-1": float('-inf'),
    "1/2-1/2": 0,
    "*": 0,
}

def negamax_r(depth=3):
    multiplier = 1 if board.turn == mychess.WHITE else -1
    
    if board.is_game_over():
        return result_values[board.result()]
        
    if depth == 0:
        return static_evaluation(board) * multiplier

    best = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        score = -negamax_r(depth-1)
        best = max(score, best)
        board.pop()
    
    return best
    
def negamax(depth=3):
    multiplier = 1 if board.turn == mychess.WHITE else -1
    
    if board.is_game_over():
        return result_values[board.result()]
        
    if depth == 0:
        return static_evaluation(board) * multiplier

    best = (None, float('-inf'))
    for move in board.legal_moves:
        board.push(move)
        score = -negamax_r(depth-1)
        if score > best[1]:
            best = (move, score)
        board.pop()
        print(move, score)
    
    return best[0]

# https://en.wikipedia.org/wiki/Principal_variation_search
def pvs():
    pass


def best_move(board: mychess.Board):
    best = (None, float('-inf'))
    for move in board.legal_moves:
        board.push(move)
        evaluation = static_evaluation(board)
        if board.turn == mychess.WHITE:
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
