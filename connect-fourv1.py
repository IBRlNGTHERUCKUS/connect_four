import copy

class State:
    def __init__ (self, parent=None, board=None):
        if not board:
            self.board = []
            for row in range(6):
                self.board.append(
                [0, 0, 0, 0, 0, 0, 0])
        else:
            self.board = board
        self.parent = parent
    def get_board_column(self, index):
        column = []
        for row in self.board:
            column.append(row[index])
        return column
    def is_terminal(self):
        if 0 not in self.board[0]:
            return True
        return False
    def get_utility(self):
        utility = 0
         #get horizontal sequences
        for row in self.board:
            utility += self.get_sequences(row)["player1"].count(4)
            utility -= self.get_sequences(row)["player2"].count(4)
        #get vertical sequences
        for i in range(7):
            utility += self.get_sequences(self.get_board_column(i))["player1"].count(4)
            utility -= self.get_sequences(self.get_board_column(i))["player2"].count(4)
        return utility
    def get_sequences(self, line):
        player1 = []
        player2 = []
        counter1 = 0
        counter2 = 0
        for val in line:
            if val == 1:
                counter1+=1
            if (val != 1 and counter1) or counter1 == 4:
                player1.append(counter1)
                counter1 = 0
            if val == 2:
                counter2+=1
            if (val != 2 and counter2) or counter2 == 4:
                player2.append(counter2)
                counter2 = 0
        player1.append(counter1)
        player2.append(counter2)

        return {
            "player1" : player1,
            "player2" : player2
            }

test = [
[0, 0, 0, 0, 0, 0, 2],
[0, 2, 0, 0, 2, 0, 1],
[2, 1, 2, 2, 1, 1, 2],
[2, 2, 2, 1, 1, 2, 2],
[1, 2, 2, 1, 2, 1, 2],
[1, 2, 1, 1, 1, 2, 1],
]
test_state = State(board = test)

def place_piece(state, index, turn):
        #invalid placement
        if state.board[0][index] != 0:
            return None
        #code to make piece "drop"
        row = 0
        while row < 5:
            if state.board[row+1][index] == 0:
                row +=1
            else:
                break

        #mark board and return new state
        new_board = copy.deepcopy(state.board)
        if turn == "A":
            new_board[row][index] = 1
        else:
            new_board[row][index] = 2
        newState = State(state, new_board)
        return newState
 
class Game_Controller:
    def __init__(self,state=State(), turn="A"):
        self.turn=turn
        self.state=state
    def toggle_turn(self):
        if self.turn == 'A':
            self.turn = 'B'
        elif self.turn == 'B':
            self.turn = 'A'
   
def print_board(board):
    for row in board:
        print(row)

    
def minimax(state, turn, depth):
    # print_board(state.board)
    # print('')
    if state.is_terminal() or depth == 0:
        return state
    elif turn == 'A':
        biggest = None
        for i in range(7):
            # print(f'parent at depth:{depth} child: {i}')
            child = place_piece(state, i, "A")
            if not child:
                continue
            recursive = minimax(child, "B", depth-1)
            if not biggest:
                biggest = recursive
                continue
            elif biggest.get_utility() < recursive.get_utility():
                biggest = recursive
                continue
        return biggest
    elif turn == 'B':
        smallest = None
        for i in range(7):
            child = place_piece(state, i, "B")
            if not child:
                continue
            recursive = minimax(child, "A", depth-1)
            if not smallest:
                smallest = recursive
                continue
            elif smallest.get_utility() > recursive.get_utility():
                smallest = recursive
                continue
        return smallest

def backtrace(start_state, end_state):
    while end_state.parent != start_state:
        end_state = end_state.parent
    return end_state
# testState = State(parent=None, board=test)
# placement_1 = place_piece(testState, 2, 'A')
# thingy = minimax(testState, "A", 2)
# print_board(backtrace(thingy).board)

#gameloop human v human
# gc = Game_Controller()
# while not gc.state.is_terminal():
#     print_board(gc.state.board)
#     print(f"It is {gc.turn}'s turn")
#     while True:
#         try:
#             column = int(input("Type a column number (0-6)"))
#         except ValueError:
#             print("must be an integer, try again")
#             break
#         if column in range(7):
#             new_state = place_piece(gc.state, column, gc.turn)
#             if new_state:
#                 gc.state = new_state
#                 gc.toggle_turn()
#                 print(f'utility: {gc.state.get_utility()}')
#                 break
#         print(f'Invalid move, try again {gc.turn}')

# gameloop AI v human
gc = Game_Controller(test_state)
while True:
    if gc.state.is_terminal():
        if gc.state.get_utility() > 0:
            print('Bot Wins')
        elif gc.state.get_utility() < 0:
            print('Human wins')
        else: 
            print('Tie')
        break
    print_board(gc.state.board)
    print(f"It is {gc.turn}'s turn")
    if gc.turn == 'B':
        try:
            column = int(input("Type a column number (0-6)"))
        except ValueError:
            print("must be an integer, try again")
            continue
        if column in range(7):
            new_state = place_piece(gc.state, column, gc.turn)
            if new_state:
                gc.state = new_state
                gc.toggle_turn()
                continue
        print(f'Invalid move, try again {gc.turn}')
    else:
        goal = minimax(gc.state, gc.turn, 3)
        next_move = backtrace(gc.state, goal)
        gc.state = next_move
        gc.toggle_turn()
        continue

# minimax(test_state, 'A', 1000000)