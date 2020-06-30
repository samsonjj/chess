import chess
import chess.svg
import chess

def write_board(board):
    with open('hello2.svg', 'w') as f:
        f.write(chess.svg.board(board=board))
        
def main():
    print("Welcome to a chess engine.")
    print("let's play a game...")
    
    board = chess.Board()
    print("Game start")
    
    write_board(board)
    while not board.is_game_over():
        move = input("Your move: ")
        try:
            board.push(board.parse_san(move))
        except:
            print("try again :(")
            continue
        write_board(board)

if __name__ == "__main__":
    main()