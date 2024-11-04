import argparse
import copy
import sys
import time

cache = {}  # you can use this to implement state caching


class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board, red, black, red_kings, black_kings):

        self.board = board

        self.width = 8
        self.height = 8
        self.num_r = red
        self.num_b = black
        self.num_r_kings = red_kings
        self.num_b_kings = black_kings
        self.initial_coords = (None, None)
        self.new_move_coords = (None, None)
        self.move_num = 0

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")

    def display_with_coords(self):
        # Print top coordinates
        print("    ", end="")
        for col in range(8):
            print(col, end=" ")
        print("")

        print("    ", end="")
        for col in range(8):
            print("_", end=" ")
        print("")

        # Print each row with its row coordinate
        for row in range(8):
            print(f"{row} |", end=" ")  # Left coordinate
            for col in range(8):
                print(self.board[row][col], end=" ")
            print("")  # Newline after each row
        print("")

    def copy(self):
        new_board = [row[:] for row in self.board]
        return State(new_board, self.num_r, self.num_b, self.num_r_kings, self.num_b_kings)

    def __str__(self):
        """
        Convert the board into a string format
        """
        string = ""
        for i, line in enumerate(self.board):
            for ch in line:
                string += ch
            string += "\n"
        return string

    def __hash__(self):
        # Create a hash based on the string representation
        board_str = ''.join([''.join(row) for row in self.board])  # Flatten the board to a string

        return hash(f"{board_str}|{self.num_r + self.num_r_kings}|{self.num_b + self.num_b_kings}")

    def __eq__(self, other):
        # Equality check based on the string representation
        return isinstance(other, State) and self.__str__() == other.__str__()

    def get_key(self, player: str, depth: int) -> str:
        board_str = ''.join([''.join(row) for row in self.board])  # Flatten the board to a string

        return f"{board_str}|{player}|{depth}"

    def update_coords(self, old_coords: tuple[int, int], new_coords: tuple[int, int]):
        self.initial_coords = old_coords
        self.new_move_coords = new_coords


def generate_successors(state: State, player: str) -> list[State]:
    """
    Generates all valid successor states for the current player by checking all possible moves and jumps.

    :param state: The current state of the checkers game.
    :param player: The current player's turn ('b' or 'r').
    :return: List of all successor states.
    """
    successors = []
    normal_directions = get_directions(player)
    king_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # King moves in all directions
    opponent = get_opp_char(player)

    for i in range(state.height):
        for j in range(state.width):
            piece = state.board[i][j]
            if piece == player.lower():  # Normal piece
                # Check all possible moves and jumps for a normal piece
                normal_moves = get_possible_moves(state, i, j, piece, opponent, normal_directions)
                successors.extend(normal_moves)
            elif piece == player.upper():  # King piece
                # Check all possible moves and jumps for a king piece
                king_moves = get_possible_moves(state, i, j, piece, opponent, king_directions)
                successors.extend(king_moves)

    # Filter all new states to only include jumps, if any
    filtered_successors = filter_jumps(state, successors, opponent)

    return filtered_successors


def filter_jumps(curr_state: State, successors: list[State], opponent: str):
    """
    Return a list of successor states corresponding to only jump moves, if any. Otherwise, return successors
    :param curr_state:
    :param successors:
    :param opponent:
    :return:
    """
    filtered = []
    for new_state in successors:
        if opponent == 'b':
            if new_state.num_b < curr_state.num_b or new_state.num_b_kings < curr_state.num_b_kings:
                filtered.append(new_state)
        else:
            if new_state.num_r < curr_state.num_r or new_state.num_r_kings < curr_state.num_r_kings:
                filtered.append(new_state)

    return filtered if filtered else successors


def get_directions(player: str) -> list[tuple[int, int]]:
    """
    Returns the movement directions for a given player.

    :param player: 'b' or 'r'
    :return: List of direction tuples representing diagonal moves (row_offset, col_offset)
    """
    if player == 'r':
        # Red pieces move diagonally up (top-left and top-right)
        return [(-1, -1), (-1, 1)]
    elif player == 'b':
        # Black pieces move diagonally down (bottom-left and bottom-right)
        return [(1, -1), (1, 1)]


def get_possible_moves(state: State, row: int, col: int, player: str, opponent: str,
                       directions: list[tuple[int, int]]) -> list[State]:
    """
    Get all possible moves for a normal piece (non-king).

    :param state: Current state of the game
    :param row: Row index of the piece
    :param col: Column index of the piece
    :param player: 'b'/'B' or 'r'/'R'
    :param opponent:
    :param directions: Movement directions for the player's normal piece
    :return: List of new states resulting from valid moves or jumps
    """
    simple = []
    jumps = []

    for direction in directions:
        new_row = row + direction[0]
        new_col = col + direction[1]

        if is_within_bounds(state, new_row + direction[0], new_col + direction[1]) and \
                state.board[new_row][new_col].lower() == opponent and \
                state.board[new_row + direction[0]][new_col + direction[1]] == '.':  # Jump over opponent's piece
            new_state = state.copy()
            new_state.board[row][col] = '.'
            new_state.board[new_row][new_col] = '.'
            new_state.board[new_row + direction[0]][new_col + direction[1]] = player
            update_counts(new_state, state.board[new_row][new_col], "jump")
            new_state.update_coords((row, col), (new_row + direction[0], new_col + direction[1]))
            new_state.move_num = state.move_num + 1

            if can_become_king(player, new_row + direction[0]):
                new_state.board[new_row + direction[0]][new_col + direction[1]] = player.upper()
                update_counts(new_state, player.upper(), "to-king")
                jumps.append(new_state)

            else:
                # After a jump, check for additional chained jumps
                chain_moves = get_chain_jumps(new_state, new_row + direction[0], new_col + direction[1],
                                              player, opponent, directions)
                if chain_moves:
                    jumps.extend(chain_moves)
                else:
                    jumps.append(new_state)

        elif is_within_bounds(state, new_row, new_col) and state.board[new_row][new_col] == '.':
            # Regular move
            new_state = state.copy()
            new_state.board[row][col] = '.'
            new_state.board[new_row][new_col] = player
            new_state.update_coords((row, col), (new_row, new_col))
            new_state.move_num = state.move_num + 1

            if can_become_king(player, new_row):
                new_state.board[new_row][new_col] = player.upper()
                update_counts(new_state, player.upper(), "to-king")

            simple.append(new_state)

    return jumps if jumps else simple


def is_within_bounds(state: State, row: int, col: int) -> bool:
    """
    Check if a given position is within the board bounds.

    :param state:
    :param row:
    :param col:
    :return:
    """
    return 0 <= row < state.height and 0 <= col < state.width


def get_chain_jumps(state: State, row: int, col: int, player: str, opponent: str,
                    directions: list[tuple[int, int]]) -> list[State]:
    """
    Recursively check for additional jumps after a jump is made (chained jumps).

    :param state: The current state after a jump
    :param row: The current row of the piece after the jump
    :param col: The current column of the piece after the jump
    :param player: The player's piece that just jumped ('b', 'r', 'B', or 'R')
    :param opponent:
    :return: A list of states if additional jumps are possible; otherwise, an empty list
    """
    chain_moves = []

    for direction in directions:
        new_row = row + direction[0]
        new_col = col + direction[1]

        if is_within_bounds(state, new_row + direction[0], new_col + direction[1]):
            if state.board[new_row][new_col].lower() == opponent \
                    and state.board[new_row + direction[0]][new_col + direction[1]] == '.':
                # Create new state
                new_state = state.copy()
                new_state.board[row][col] = '.'
                new_state.board[new_row][new_col] = '.'
                new_state.board[new_row + direction[0]][new_col + direction[1]] = player
                update_counts(new_state, state.board[new_row][new_col], "jump")
                new_state.update_coords((row, col), (new_row + direction[0], new_col + direction[1]))
                new_state.move_num = state.move_num + 1

                if can_become_king(player, new_row + direction[0]):
                    new_state.board[new_row + direction[0]][new_col + direction[1]] = player.upper()
                    update_counts(new_state, player.upper(), "to-king")
                    chain_moves.append(new_state)

                else:
                    additional_jumps = get_chain_jumps(new_state, new_row + direction[0], new_col + direction[1],
                                                       player, opponent, directions)
                    if additional_jumps:
                        chain_moves.extend(additional_jumps)
                    else:
                        chain_moves.append(new_state)

    return chain_moves


def update_counts(new_state: State, piece: str, move_type: str):
    """

    :param new_state:
    :param piece:
    :param move_type:
    :return:
    """
    if move_type == "jump":
        if piece == 'b':
            new_state.num_b -= 1
        elif piece == 'B':
            new_state.num_b_kings -= 1
        elif piece == 'r':
            new_state.num_r -= 1
        elif piece == 'R':
            new_state.num_r_kings -= 1
    elif move_type == "to-king":
        if piece == 'B':
            new_state.num_b_kings += 1
            new_state.num_b -= 1
        elif piece == 'R':
            new_state.num_r_kings += 1
            new_state.num_r -= 1


def can_become_king(piece: str, row: int) -> bool:
    """

    :param piece:
    :param row:
    :return:
    """
    if piece == 'b':
        return row == 7
    elif piece == 'r':
        return row == 0
    return False


def game_over(state: State) -> bool:
    """
    Check if the current player has won the game.

    :param state: The current state of the checkers game
    :return: True if game is over, False otherwise
    """
    return state.num_r + state.num_r_kings == 0 or state.num_b + state.num_b_kings == 0


def is_winner(state: State, player: str):
    """

    :param state: The current state of the checkers game
    :param player: The player to check for a win ('b' or 'r')
    :return: True if player has won, False otherwise
    """
    opponent = get_opp_char(player)

    # Check if opponent has pieces left
    if opponent == 'b':
        if state.num_b + state.num_b_kings == 0:
            return True
    else:
        if state.num_r + state.num_r_kings == 0:
            return True

    # # Check if opponent has no valid moves left
    # opponent_moves = generate_successors(state, opponent)
    # return not opponent_moves


def get_opp_char(player: str) -> str:
    if player in ['b', 'B']:
        return 'r'
    else:
        return 'b'


def get_next_turn(curr_turn: str) -> str:
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'


def utility(state: State, depth: int):
    """

    :param state:
    :param depth:
    :return:
    """
    if is_winner(state, 'b'):
        return 1000000 - depth  # Favor shorter wins
    if is_winner(state, 'r'):
        return -1000000 + depth  # Delay losses
    # Use evaluation function for non-terminal nodes
    return evaluate(state)


def evaluate(state: State):
    """

    :param state:
    :return:
    """
    red_score = state.num_r + state.num_r_kings * 2
    black_score = state.num_b + state.num_b_kings * 2
    return black_score - red_score


def limited_minimax_alphabeta(state: State, player: str, depth: int, alpha: float, beta: float) -> tuple:
    """
    Performs depth-limited minimax with alpha-beta pruning, caching, and node ordering.

    :param state: The current state of the checkers game.
    :param player: The player whose turn it is ('r' or 'b').
    :param depth: The current depth in the search tree.
    :param alpha: The best value that the maximizer can guarantee.
    :param beta: The best value that the minimizer can guarantee.
    :return: The best move and its associated utility value.
    """
    if game_over(state) or depth == 10:
        # Return the utility value of the state if it's a terminal state or depth limit reached
        return state, utility(state, depth)

    # Check if the state has already been evaluated
    state_key = state.get_key(player, depth)
    if state_key in cache and depth > 0:
        return cache[state_key]

    best_move = None
    if player == 'b':
        value = -float('inf')  # Maximizer's goal
        successors = generate_successors(state, player)

        # Sort successors based on heuristic or value (for node ordering)
        successors.sort(key=lambda x: utility(x, depth), reverse=True)

        for move in successors:
            next_value = limited_minimax_alphabeta(move, get_opp_char(player), depth + 1, alpha, beta)[1]
            if next_value > value:
                value = next_value
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Prune!
    else:
        value = float('inf')  # Minimizer's goal
        successors = generate_successors(state, player)

        # Sort successors based on heuristic or value (for node ordering)
        successors.sort(key=lambda x: utility(x, depth))

        for move in successors:
            next_value = limited_minimax_alphabeta(move, get_opp_char(player), depth + 1, alpha, beta)[1]
            if next_value < value:
                value = next_value
                best_move = move
            beta = min(beta, value)
            if alpha >= beta:
                break  # Prune!

    # Cache the evaluated state and its utility value
    if depth > 0:
        cache[state_key] = (best_move, value)

    return best_move, value


def count_pieces(board) -> tuple[int, int, int, int]:
    """

    :param board:
    :return:
    """
    r, b, r_kings, b_kings = 0, 0, 0, 0
    for i in board:
        for j in i:
            if j == 'r':
                r += 1
            elif j == 'R':
                r_kings += 1
            elif j == 'b':
                b += 1
            elif j == 'B':
                b_kings += 1
    return r, b, r_kings, b_kings


def read_from_file(filename):
    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board


def get_user_moves_dict(successors: list[State]) -> dict[str, list[tuple]]:
    moves_dict = {}    
    for new_state in successors:
        key = f"{new_state.initial_coords[0]},{new_state.initial_coords[1]}"
        if key in moves_dict:
            moves_dict[key].append(list(new_state.new_move_coords))
        else:
            moves_dict[key] = [list(new_state.new_move_coords)]
    return moves_dict


if __name__ == '__main__':

    # Initialize board and game state
    initial_board = [
        ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
        ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
        ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['r', '.', 'r', '.', 'r', '.', 'r', '.'],
        ['.', 'r', '.', 'r', '.', 'r', '.', 'r'],
        ['r', '.', 'r', '.', 'r', '.', 'r', '.']
    ]  # Set up the initial board configuration
    state = State(initial_board, red=12, black=12, red_kings=0, black_kings=0)
    winner = ""
    curr_player = 'r'

    print("***Welcome to Checkers! You are playing as Red.***\n")

    state.display_with_coords()

    while not game_over(state):
        if curr_player == 'r':
            # User's turn
            print("Choose a move:")
            # state.display()

            user_moves = generate_successors(state, 'r')
            if user_moves:
                for i in range(len(user_moves)):
                    print(f"Move {i+1}: {user_moves[i].initial_coords} to  {user_moves[i].new_move_coords}")

                move = int(input("\nEnter your move number: "))
                state = user_moves[move-1]

            print("\nYour move:", state.move_num)
            state.display_with_coords()

            # Check for game over after user's move
            if game_over(state):
                print("Game over! You won!")
                winner = 'r'
                break

        elif curr_player == 'b':
            # AI's turn
            print("AI's move:")
            alpha = -1000000  # -float('inf')
            beta = 1000000  # float('inf')

            ai_move = limited_minimax_alphabeta(state, 'b', 0, alpha, beta)[0]
            state = ai_move
            state.display_with_coords()

            # Check for game over after AI's move
            if game_over(state):
                print("Game over! The AI won!")
                winner = 'b'
                break

        curr_player = get_next_turn(curr_player)

    print(f"WINNER: {winner}")
