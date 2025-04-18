import copy
import random
import eval


class State:
    def __init__(self, parent=None, board=None, turn="A"):
        self.board = board
        if not self.board:
            self.board = []
            for row in range(6):
                self.board.append([0, 0, 0, 0, 0, 0, 0])
        self.parent = parent
        self.turn = turn

    def is_terminal(self):
        if self.board[0].count(0) == 0:
            return True

    def place_piece(self, column):
        if column not in range(0, 7) or self.board[0][column] != 0:
            return None
        row = 0
        while row < 5 and self.board[row + 1][column] == 0:
            row += 1
        new_board = copy.deepcopy(self.board)
        if self.turn == "A":
            new_board[row][column] = 1
            return State(self, new_board, "B")
        else:
            new_board[row][column] = 2
            return State(self, new_board, "A")


test = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 0, 1, 2, 0],
    [1, 1, 2, 2, 2, 1, 2],
    [1, 1, 1, 2, 1, 2, 2],
]
# test = [
#     [2, 2, 2, 1, 1, 1, 1],
#     [1, 2, 1, 2, 1, 2, 1],
#     [1, 2, 2, 1, 2, 1, 1],
#     [1, 1, 2, 2, 1, 2, 1],
#     [1, 1, 2, 2, 2, 2, 2],
#     [1, 1, 1, 2, 2, 2, 2],
# ]

# Human v Random opponent
# class Game_Controller:
#     def __init__(self, state=State()):
#         self.state = state

#     def game_loop(self):
#         while True:
#             if self.state.is_terminal():
#                 if eval.board_utility(self.state.board) > 0:
#                     print("Player 1 wins")
#                 elif eval.board_utility(self.state.board) == 0:
#                     print("Tie")
#                 else:
#                     print("Player 2 wins")
#                 return
#             if self.state.turn == "A":
#                 while True:
#                     column = int(input("Player 1 enter a column between 0 and 6"))
#                     placement = self.state.place_piece(column)
#                     if placement:
#                         self.state = placement
#                         break
#             else:
#                 while True:
#                     column = random.randint(0, 5)
#                     placement = self.state.place_piece(column)
#                     if placement:
#                         self.state = placement
#                         break
#             print_board(self.state.board)

# Human v AI
# Player 1 = AI
# Player 2 = Human
# class Game_Controller:
#     def __init__(self, state=State(turn="B")):
#         self.state = state

#     def game_loop(self):
#         while True:
#             if self.state.is_terminal():
#                 if eval.board_utility(self.state.board) > 0:
#                     print("Player 1 wins")
#                 elif eval.board_utility(self.state.board) == 0:
#                     print("Tie")
#                 else:
#                     print("Player 2 wins")
#                 return
#             if self.state.turn == "A":
#                 next_move = backtrace(self.state, minimax(self.state, 4))
#                 gc.state = next_move
#             elif self.state.turn == "B":
#                 while True:
#                     column = int(input("Player 1 enter a column between 0 and 6"))
#                     placement = self.state.place_piece(column)
#                     if placement:
#                         self.state = placement
#                         break
#             print_board(self.state.board)
# Human v AI
# Player 1 = AI
# Player 2 = Random
class Game_Controller:
    def __init__(self, state=State(turn="B")):
        self.state = state

    def game_loop(self):
        while True:
            if self.state.is_terminal():
                if eval.board_utility(self.state.board) > 0:
                    print("Player 1 wins")
                elif eval.board_utility(self.state.board) == 0:
                    print("Tie")
                else:
                    print("Player 2 wins")
                return
            if self.state.turn == "A":
                next_move = backtrace(self.state, minimax(self.state, 3))
                gc.state = next_move
            elif self.state.turn == "B":
                while True:
                    column = random.randint(0,6)
                    placement = self.state.place_piece(column)
                    if placement:
                        self.state = placement
                        break
            print_board(self.state.board)

def print_board(board):
    for row in board:
        print(row)
    print("")

#Player 1 is AI
#Player 2 is Human
def minimax(state, depth):
    if state.is_terminal() or depth == 0:
        return state
    elif state.turn == "A":  # max player turn
        # find the child node with the largest utility recursively
        biggest = None
        for i in range(7):
            child = state.place_piece(i)
            # skip if the move is invalid
            if not child:
                continue
            recursive = minimax(child, depth - 1)
            if not biggest:
                biggest = recursive
                continue
            elif eval.evaluate_board(biggest.board) < eval.evaluate_board(recursive.board):
                biggest = recursive
                continue
        return biggest
    elif state.turn == "B":  # min player turn
        # find the child node with the smallest utility recursively
        smallest = None
        for i in range(7):
            child = state.place_piece(i)
            # skip if the move is invalid
            if not child:
                continue
            recursive = minimax(child, depth - 1)
            if not smallest:
                smallest = recursive
                continue
            elif eval.evaluate_board(smallest.board) < eval.evaluate_board(recursive.board):
                smallest = recursive
        return smallest

def backtrace(start_state, end_state):
    while end_state.parent != start_state:
        end_state = end_state.parent
    return end_state
for i in range(10):
    gc = Game_Controller()
    gc.game_loop()
