from game_main import Sudoku_Game
import data_model

if __name__ == "__main__":
    board = data_model.create_sudoku_task()
    game = Sudoku_Game(board=board)
    game.run()