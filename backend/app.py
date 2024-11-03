from flask import Flask, request, jsonify
from flask_cors import CORS
import checkers_ai  # Import AI logic

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
]

curr_state = checkers_ai.State(initial_board, 12, 12, 0, 0)

@app.route('/user_move', methods=['POST'])
def user_moves():
    """Endpoint to get all possible moves for the user."""

    # Generate all possible successor states for the user (red pieces)
    successors = checkers_ai.generate_successors(curr_state, 'r')
    user_moves_dict = checkers_ai.get_user_moves_dict(successors)

    # Send user moves to frontend
    return jsonify({"user_moves": user_moves_dict}), 200


@app.route('/apply_user_move', methods=['POST'])
def apply_user_move():
    """Endpoint to apply user's move"""
    try:
        # Get user-move info from frontend
        data = request.json
        old_coords = data.get('old_coords')
        new_coords = data.get('new_coords')
        piece = data.get('piece')

        print(old_coords, new_coords, piece)

        if not all([old_coords, new_coords, piece]):
            return jsonify({"error": "Missing required parameters"}), 400

        directions = [(-1, -1), (-1, 1)] if piece == 'r' else [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves = checkers_ai.get_possible_moves(curr_state, old_coords[0], old_coords[1], piece, 'b', directions)

        for new_state in moves:
            if new_state.initial_coords == old_coords and new_state.new_move_coords == new_coords:
                curr_state = new_state
                break
        
        num_red = curr_state.num_r + curr_state.num_r_kings
        num_black = curr_state.num_b + curr_state.num_b_kings

        return jsonify({"board_state": curr_state.board, "num_red": num_red, "num_black": num_black})

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500
    

@app.route('/ai_move', methods=['POST'])
def ai_move():
    """Endpoint to get AI's next move."""

    # Set up parameters for alpha-beta pruning
    alpha = -1000000  # -float('inf')
    beta = 1000000  # float('inf')

    # Compute AI's move
    ai_move = checkers_ai.limited_minimax_alphabeta(curr_state, 'b', 0, alpha, beta)[0]

    if ai_move is None:
        return jsonify({"ai_move": [], "board_state": [], "num_red": None, "num_black": None}), 200

    # Extract move coordinates for the AI's move
    ai_move_coords = [ai_move.initial_coords, ai_move.new_move_coords]

    # Update curr_state to reflect AI's move
    curr_state = ai_move
    num_red = curr_state.num_r + curr_state.num_r_kings
    num_black = curr_state.num_b + curr_state.num_b_kings

    # Send AI's move to frontend
    return jsonify({"ai_move": ai_move_coords, "board_state": ai_move.board, "num_red": num_red, "num_black": num_black}), 200

if __name__ == '__main__':
    app.run(debug=True)
