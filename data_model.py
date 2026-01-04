from pydantic import BaseModel, Field
import random
 
class Sudoku_Game(BaseModel):
    """
    Aufgabe 3:
    pygame developer should design this
    """
    board: list[list[int]]
    duration: int = Field(description="How long a game takes")
    ### additional fields
 
 
# 4 rules/functions
def rule_check_row(row: list[int]) -> bool:
    seen: set[int] = set()
    for value in row:
        if value == 0:
            continue
        if value in seen:
            return False
        seen.add(value)
 
    return True
 
def rule_check_column(column: list[int]) -> bool:
    seen: set[int] = set()
    for value in column:
        if value == 0:
            continue
        if value in seen:
            return False
        seen.add(value)
 
    return True
 
def rule_check_3x3_box(box: list[list[int]]) -> bool:
    seen: set[int] = set()
    for row in box:
        for value in row:
            if value == 0:
                continue
            if value in seen:                                            
                return False
            seen.add(value)
 
    return True
 
def rule_check_whole_board(board: list[list[int]]) -> bool:
    for i in range(9):
        if not rule_check_row(board[i]):
            return False
 
        column = [board[j][i] for j in range(9)]
        if not rule_check_column(column):
            return False
 
        box_row = i // 3
        box_col = i % 3
        box = [
            board[r][box_col * 3:(box_col + 1) * 3]
            for r in range(box_row * 3, (box_row + 1) * 3)
        ]
        if not rule_check_3x3_box(box):
            return False
 
    return True

def check_game_won(board: list[list[int]]) -> bool:
    for row in board:
        if any(value == 0 for value in row):
            return False
    return rule_check_whole_board(board)
 
 

def create_sudoku_task() -> list[list[int]]:
    """
    Mittelschwere Sudoku-Aufgaben (mehr Logik, weniger offensichtliche Felder).
    Rückgabe: 9x9 Board mit 0 = leeres Feld
    """
    boards = [


        [
            [0, 0, 3, 0, 2, 0, 6, 0, 0],
            [9, 0, 0, 3, 0, 0, 0, 0, 1],
            [0, 0, 1, 8, 0, 6, 4, 0, 0],
            [0, 0, 8, 1, 0, 2, 9, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 6, 7, 0, 8, 2, 0, 0],
            [0, 0, 2, 6, 0, 9, 5, 0, 0],
            [8, 0, 0, 0, 0, 5, 0, 0, 7],
            [0, 0, 5, 0, 1, 0, 3, 0, 0],
        ],


        [
            [0, 0, 0, 2, 6, 0, 7, 0, 1],
            [6, 0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 7, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 0, 0, 6, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],


        [
            [4, 0, 0, 0, 0, 0, 6, 0, 7],
            [0, 8, 0, 0, 1, 0, 5, 2, 0],
            [0, 0, 0, 0, 0, 7, 0, 0, 3],
            [0, 0, 7, 3, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 4],
            [5, 0, 0, 0, 0, 1, 7, 0, 0],
            [2, 0, 0, 6, 0, 0, 0, 0, 0],
            [0, 7, 4, 0, 5, 0, 0, 3, 0],
            [1, 0, 8, 0, 0, 0, 0, 0, 6],
        ],

        [
            [0, 3, 0, 0, 0, 0, 0, 7, 0],
            [0, 0, 0, 4, 0, 1, 0, 0, 8],
            [7, 0, 0, 0, 0, 5, 0, 2, 0],
            [0, 0, 2, 0, 3, 0, 0, 0, 5],
            [0, 0, 0, 1, 0, 6, 0, 0, 0],
            [3, 0, 0, 0, 7, 0, 1, 0, 0],
            [0, 2, 0, 5, 0, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 9, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 1, 0],
        ],

        [
            [0, 0, 6, 0, 0, 4, 0, 9, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 7, 0, 0, 0, 1, 5, 0, 0],
            [0, 0, 3, 4, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 0, 6, 0],
            [0, 1, 0, 0, 0, 6, 3, 0, 0],
            [0, 0, 4, 1, 0, 0, 0, 7, 0],
            [3, 0, 0, 0, 6, 0, 0, 0, 0],
            [0, 6, 0, 9, 0, 0, 1, 0, 0],
        ],

        [
            [8, 0, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 6, 0, 2, 0, 0, 0],
            [0, 7, 0, 0, 3, 0, 0, 0, 9],
            [0, 0, 1, 0, 0, 7, 3, 0, 0],
            [0, 4, 0, 8, 0, 3, 0, 5, 0],
            [0, 0, 2, 5, 0, 0, 1, 0, 0],
            [2, 0, 0, 0, 6, 0, 0, 1, 0],
            [0, 0, 0, 4, 0, 9, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 6],
        ],
    ]

    return random.choice(boards)
 