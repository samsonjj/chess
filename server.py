import webbrowser
import os
from flask import Flask, send_from_directory, abort, request, Response
from flask_cors import CORS
from mychess import try_move, negamax, board, update

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