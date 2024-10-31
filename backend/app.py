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
    try:
        # Get current game-state from frontend
        data = request.json
        board = data.get('board_state')
        num_r = data.get('num_red_pieces')
        num_r_kings = data.get('num_red_kings')
        num_b = data.get('num_black_pieces')
        num_b_kings = data.get('num_black_kings')

        if not (board and num_r and num_b and num_r_kings and num_b_kings):
            return jsonify({"error": "State info is required"}), 400
        
        state = checkers_ai.State(board, num_r, num_b, num_r_kings, num_b_kings)

        # Generate all possible successor states for the user (red pieces)
        successors = checkers_ai.generate_successors(state, 'r')
        user_moves_dict = checkers_ai.get_user_moves_dict(successors)

        # Send user moves to frontend
        return jsonify({"user_moves": user_moves_dict}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500
    

@app.route('/apply_user_move', methods=['POST'])
def apply_user_move():
    """Endpoint to apply user's move"""
    

@app.route('/ai_move', methods=['POST'])
def ai_move():
    """Endpoint to get AI's next move."""
    try:
        # Get current game-state from frontend
        data = request.json
        board = data.get('board_state')
        num_r = data.get('num_red_pieces')
        num_r_kings = data.get('num_red_kings')
        num_b = data.get('num_black_pieces')
        num_b_kings = data.get('num_black_kings')

        if not (board and num_r and num_b and num_r_kings and num_b_kings):
            return jsonify({"error": "State info is required"}), 400

        state = checkers_ai.State(board, num_r, num_b, num_r_kings, num_b_kings)

        # Set up parameters for alpha-beta pruning
        alpha = -1000000  # -float('inf')
        beta = 1000000  # float('inf')

        # Compute AI's move
        ai_move = checkers_ai.limited_minimax_alphabeta(state, 'b', 0, alpha, beta)[0]

        # Extract move coordinates for the AI's move
        ai_move_coords = [ai_move.initial_coords, ai_move.new_move_coords]

        # Send AI's move to frontend
        return jsonify({"ai_move": ai_move_coords}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
