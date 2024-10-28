from flask import Flask, render_template, jsonify, request
import ai_checkers  # Import your Checkers game logic here

app = Flask(__name__)

# Route to render the main Checkers board
@app.route('/')
def index():
    return render_template('index.html')  # Your main game frontend

# API route to process a move
@app.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    # Process the move with your game logic here, e.g., checkers_logic.process_move(data)
    response = {"status": "success", "message": "Move processed"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
