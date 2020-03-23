from collections import Set, OrderedDict
import copy
import time
import statistics
import sys

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"

b1 = {'A1','A2','A3','B1','B2','B3','C1','C2','C3'}
b2 = {'D1','D2','D3','E1','E2','E3','F1','F2','F3'}
b3 = {'G1','G2','G3','H1','H2','H3','I1','I2','I3'}
b4 = {'A4','A5','A6','B4','B5','B6','C4','C5','C6'}
b5 = {'D4','D5','D6','E4','E5','E6','F4','F5','F6'}
b6 = {'G4','G5','G6','H4','H5','H6','I4','I5','I6'}
b7 = {'A7','A8','A9','B7','B8','B9','C7','C8','C9'}
b8 = {'D7','D8','D9','E7','E8','E9','F7','F8','F9'}
b9 = {'G7','G8','G9','H7','H8','H9','I7','I8','I9'}
boxes = [b1, b2, b3, b4, b5, b6, b7, b8, b9]


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def is_complete(board):
    if board['zeros'] == 0:
        return True
    return False


def add_zeros_key(board):
    zero_count = 0
    for val in board.values():
        if val == 0:
            zero_count += 1
    board['zeros'] = zero_count
    return board


def add_possible_values(board):
    new_board = board.copy()
    del board['zeros']
    for key in board:
        possible_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        if board[key] != 0:
            continue
        letter = key[0]
        number = key[1]

        # row : letter
        for n in range(1, 10):
            current = letter+str(n)
            val = board[current]
            if val != 0:
                possible_values.discard(val)

        # column : number
        for L in ROW:
            current = str(L+number)
            val = board[current]
            if val != 0:
                possible_values.discard(val)

        # box
        for box in boxes:
            if key in box:
                for current in box:
                    val = board[current]
                    possible_values.discard(val)
                break

        new_board[key] = possible_values

    costs = {}
    for key in new_board:
        val = new_board[key]
        if isinstance(val, Set):
            cost = len(val)
            if cost in costs:
                costs[cost].add(key)
            else:
                costs[cost] = {key}
    for cost in range(1,10):
        if cost not in costs:
            costs[cost] = set()

    costs = OrderedDict(sorted(costs.items()))

    new_board['costs'] = costs

    return new_board


def forward_check(board, var, assignment):

    cost = len(board[var])
    board[var] = assignment
    letter = var[0]
    number = var[1]

    # row : letter
    for n in range(1, 10):
        current = letter + str(n)
        val = board[current]
        if isinstance(val, Set):
            if assignment in board[current]:
                current_cost = len(val)
                board['costs'][current_cost].discard(current)
                board[current].discard(assignment)
                if len(board[current]) == 0:
                    return False
                board['costs'][current_cost - 1].add(current)

    # column : number
    for L in ROW:
        current = str(L + number)
        val = board[current]
        if isinstance(val, Set):
            if assignment in board[current]:
                current_cost = len(val)
                board['costs'][current_cost].discard(current)
                board[current].discard(assignment)
                if len(board[current]) == 0:
                    return False
                board['costs'][current_cost - 1].add(current)

    # box
    for box in boxes:
        if var in box:
            for current in box:
                val = board[current]
                if isinstance(val, Set):
                    if assignment in board[current]:
                        current_cost = len(val)
                        board['costs'][current_cost].discard(current)
                        board[current].discard(assignment)
                        if len(board[current]) == 0:
                            return False
                        board['costs'][current_cost - 1].add(current)
            break

    board['zeros'] -= 1
    board['costs'][cost].discard(var)
    return board


def choose_next_var(board):
    for cost in board['costs']:
        if len(board['costs'][cost]) != 0:
            return next(iter(board['costs'][cost]))


def backtracking(board):
    """Takes a board and returns solved board."""
    board = add_zeros_key(board)
    board = add_possible_values(board)
    solved_board = backtrack_helper(board)
    del solved_board['costs']
    del solved_board['zeros']
    return solved_board


def backtrack_helper(board):
    if is_complete(board):
        return board

    next_var = choose_next_var(board)
    for val in board[next_var]:
        sd = copy.deepcopy(board)
        f_c = forward_check(board, next_var, val)
        if f_c is not False:
            result = backtrack_helper(f_c)
            if result is not False:
                return result
        board = sd

    return False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        start_board = sys.argv[1]
    else:
        print("Provided command-line argument!")
        sys.exit()

    if len(start_board) < 9:
        sys.exit()

    # Parse boards to dict representation, scanning board L to R, Up to Down
    board = { ROW[r] + COL[c]: int(start_board[9*r+c]) for r in range(9) for c in range(9)}

    print_board(board)
    start = time.time()
    solved_board = backtracking(board)
    print_board(solved_board)

    print("-----------------\n\nTime to complete:", round((time.time()-start),3), "seconds\n")

