from shell import ShellThread
import chess
import chess.svg
import webbrowser
import os
import random
from flask import Flask, send_from_directory, abort, request, Response
from flask_cors import CORS

TEMP_SVG_PATH = './images/temp.svg'

def save_svg(board, url=TEMP_SVG_PATH):
    with open(TEMP_SVG_PATH, 'w') as f:
        f.write(chess.svg.board(board=board))


def try_move(board: chess.Board, move):
    try:
        board.push(board.parse_san(move))
        return True
    except:
        return False

board = chess.Board()
def update():
    save_svg(board)

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 10
}

def static_evaluation(board):
    evaluation = 0
    for square, piece in board.piece_map().items():
        multiplier = 1 if piece.color == chess.WHITE else -1

        value = piece_values[piece.piece_type]
        evaluation += multiplier * value
        if piece.piece_type == chess.PAWN and square in [chess.D5, chess. D4, chess.E4, chess.E5]:
            evaluation += multiplier * .1
    return evaluation

# class Node:
#     def __init__(self, score):
#         self.score = 0
#         self.children = []

result_values = {
    "1-0": float('inf'),
    "0-1": float('-inf'),
    "1/2-1/2": 0,
    "*": 0,
}

def negamax_r(depth=3):
    # print(depth)
    multiplier = 1 if board.turn == chess.WHITE else -1
    
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
    multiplier = 1 if board.turn == chess.WHITE else -1
    
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
    

app = Flask(__name__)
CORS(app)

@app.get("/image")
def get_image():
    try:
        return send_from_directory('./images', 'temp.svg')
    except FileNotFoundError:
        abort(404)

@app.post("/move")
def send_move():
    print(request.json)
    if not try_move(board, request.json["move"]):
        return Response(status=400)
    else:
        update()
        if not board.is_game_over():
            board.push(negamax(3)) 
            update()
        return Response(status=201)
    
webbrowser.open('file://' + os.path.realpath('index.html'))
update()

if __name__ == "__main__":
    pass
    update()
    webbrowser.open('file://' + os.path.realpath('index.html'))
    running = True
    while running:
        user_input = input('> ')
        if not try_move(board, user_input):
            print('invalid move :(')
            continue
        else:
            update()
        if board.is_game_over():
            print('You win! (or lose)')
            print(board.result())
            break
        move = negamax(3)
        print('      ' + str(move))
        board.push(move)
        update()
        print(board.promoted)
