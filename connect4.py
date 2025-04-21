import copy
import random
import eval
import sys

def print_board(board):
    for row in board:
        print(row)
    print("")

class State:
    def __init__(self, parent=None, board=None, player=2):
        self.board = board
        self.parent = parent
        self.player = player
        if not self.board:
            self.board = []
            for row in range(6):
                self.board.append([0, 0, 0, 0, 0, 0, 0])

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
        if self.player == "A":
            new_board[row][column] = 1
            return State(self, new_board, "B")
        else:
            new_board[row][column] = 2
            return State(self, new_board, "A")
#Player 1 is AI
#Player 2 is Human
def minimax(state, turn, depth):
    if state.is_terminal() or depth == 0:
        return state
    elif turn == "computer-next":  # max player turn
        # find the child node with the largest utility recursively
        biggest = None
        for i in range(7):
            child = state.place_piece(i)
            # skip if the move is invalid
            if not child:
                continue
            recursive = minimax(child, "human-next", depth - 1)
            if not biggest:
                biggest = recursive
                continue
            elif eval.evaluate_board(biggest.board) < eval.evaluate_board(recursive.board):
                biggest = recursive
                continue
        return biggest
    elif turn == "human-next":  # min player turn
        # find the child node with the smallest utility recursively
        smallest = None
        for i in range(7):
            child = state.place_piece(i)
            # skip if the move is invalid
            if not child:
                continue
            recursive = minimax(child, "computer-next", depth - 1)
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

def interactive_mode(state, turn, depth):
    while not state.is_terminal():  
        if turn == "computer-next":
            score = eval.get_score(state.board)
            print_board(state.board)
            print(f'{score[0]} : {score[1]}')
            next_move = backtrace(state, minimax(state, turn, depth))
            state = next_move
            turn = "human-next"
        elif turn == "human-next":
            score = eval.get_score(state.board)
            print_board(state.board)
            print(f'{score[0]} : {score[1]}')
            while True:
                try:
                    col = int(input("Enter a number between 0 and 6\n"))
                except ValueError:
                    print('Invalid input')
                    continue
                # col = random.randint(0,6)
                next_move = state.place_piece(col)
                # check if placement is valid
                if next_move:
                    state = next_move
                    turn = "computer-next"
                    break
                print("Invalid input\n")

def one_move_mode(state, turn, depth, output_file):
    # Determine if the max player is 1 or 2
    if turn == "computer-next":
        max_player = state.player
    elif turn == "human-next":
        if state.player == 1:
            max_player = 2
        else:
            max_player = 1
    #print current state and score
    score = eval.get_score(state.board)
    print_board(state.board)
    print(f'{score[0]} : {score[1]}')
    #make the next move
    if not state.is_terminal():
        next_move = backtrace(state, minimax(state, turn, depth, max_player))
        state = next_move
    #print new state and score
    score = eval.get_score(state.board)
    print_board(state.board)
    print(f'{score[0]} : {score[1]}')
    #save the new state
    save_state(state, output_file)
        

# if len(sys.argv) == 5:
if (True):
    #initialize the board
    board = []
    # input_file = open(sys.argv[2], 'r')
    # for x in range(6):
        # board.append(list(input_file.readline())[0:6])
    # player = input_file.readline()
    # state = State(None, board, player)
    #interactive mode
    # if sys.argv[1] == 'interactive':
        # interactive_mode(state, sys.argv[3], sys.argv[4])
    interactive_mode(State(player="A"), "computer-next", 3)

