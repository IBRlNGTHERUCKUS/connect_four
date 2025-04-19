def get_down_diagonal(board, start_x, start_y):
    diagonal = []
    y = start_y
    x = start_x
    while y < 6 and x < 7:
        diagonal.append(board[y][x])
        y+=1
        x+=1
    return diagonal
    
def get_up_diagonal(board, start_x, start_y):
    diagonal = []
    y = start_y
    x = start_x
    while y >= 0 and x < 7:
        diagonal.append(board[y][x])
        y-=1
        x+=1
    return diagonal
    
def get_column(board, x):
    column = []
    for y in range(6):
        column.append(board[y][x])
    return column

def evaluate_array(arr):
    eval = 0
    p1_seq, p2_seq = [],[]
    for el in arr:
        if el == 0:
                p1_seq.append(el)
                p2_seq.append(el)
        elif el == 1:
            p1_seq.append(el)
            p2_seq = []
        elif el == 2:
            p2_seq.append(el)
            p1_seq = []
        p1_len, p2_len = len(p1_seq), len(p2_seq)
        if p1_len == 4:
            eval += p1_seq.count(1) ** 2
            p1_seq.pop(0)
        if p2_len == 4:
            eval -= p2_seq.count(2) ** 2
            p2_seq.pop(0)
    return eval
    
def evaluate_board(board):
    total_eval = 0
    #evaluate down diagonals
    diag_coords = [[0,2],[0,1],[0,0],[1,0],[2,0],[3,0]]
    for coord in diag_coords:
        total_eval += evaluate_array(get_down_diagonal(board, coord[0], coord[1]))
    #evaluate up diagonals
    diag_coords = [[0,3],[0,4],[0,5],[1,5],[2,5],[3,5]]
    for coord in diag_coords:
        total_eval += evaluate_array(get_up_diagonal(board, coord[0], coord[1]))
    #evaluate columns
    for i in range(7):
        #print(f'column {i}')
        total_eval += evaluate_array(get_column(board, i))
    #evaluate rows
    for i in range(6):
        #print(f'row {i}')
        total_eval += evaluate_array(board[i])
    return total_eval
    
def array_utility(arr):
    p1_seq, p2_seq = [],[]
    for el in arr:
        if el == 1:
            p1_seq.append(el)
            p2_seq = []
        elif el == 2:
            p2_seq.append(el)
            p1_seq = []
        p1_len, p2_len = len(p1_seq), len(p2_seq)
        if p1_len == 4:
            return 1
        if p2_len == 4:
            return -1
    return 0
                     
def get_score(board):
    scores = []
    #evaluate down diagonals
    diag_coords = [[0,2],[0,1],[0,0],[1,0],[2,0],[3,0]]
    for coord in diag_coords:
        scores.append(array_utility(get_down_diagonal(board, coord[0], coord[1])))
    #evaluate up diagonals
    diag_coords = [[0,3],[0,4],[0,5],[1,5],[2,5],[3,5]]
    for coord in diag_coords:
        scores.append(array_utility(get_up_diagonal(board, coord[0], coord[1])))
    #evaluate columns
    for i in range(7):
        #print(f'column {i}')
        scores.append(array_utility(get_column(board, i)))
    #evaluate rows
    for i in range(6):
        #print(f'row {i}')
        scores.append(array_utility(board[i]))
    p1_score = scores.count(1)
    p2_score = scores.count(-1)
    return [p1_score, p2_score]             
                
test1 = [
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0],
[2, 0, 0, 1, 0, 0, 0],
[2, 0, 0, 1, 1, 0, 0],
[2, 2, 0, 1, 1, 0, 0],
]
test2 = [
[0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0],
[1, 0, 0, 2, 0, 0, 0],
[2, 0, 0, 1, 0, 0, 0],
[2, 0, 0, 1, 1, 0, 0],
[2, 2, 0, 1, 1, 0, 0],
]

print(evaluate_board(test1))
print(evaluate_board(test2))