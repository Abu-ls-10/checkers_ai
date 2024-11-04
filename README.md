# CheckersAI

An interactive Checkers game powered by an AI opponent. This project features a sleek user interface with turn-based gameplay, where users can challenge an AI opponent that makes optimal moves based on implemented strategies. The project is developed using a React frontend and Flask backend, making use of AI algorithms to simulate intelligent gameplay.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [API Endpoints](#api-endpoints)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Overview

CheckersAI is designed to be an engaging and challenging experience for users who want to play against an AI. The AI utilizes algorithms such as **alpha-beta pruning** for move selection, making it competitive even at advanced stages of the game. The frontend is built with **React** for an interactive game experience, and the backend, developed in **Flask**, processes moves and determines the AI's responses.

## Features

- **Interactive Gameplay**: A visually appealing Checkers board with drag-and-drop functionality for piece movement.
- **AI Opponent**: An AI player that computes optimal moves using alpha-beta pruning, ensuring challenging gameplay.
- **Real-time Game State Updates**: The board state is updated after every move, keeping track of player pieces and remaining moves.
- **Responsive Design**: UI is optimized for desktop and mobile devices.
- **Move History**: Track the moves made by both the user and the AI.

## Tech Stack

- **Frontend**: React, CSS
- **Backend**: Flask, Python
- **API Requests**: Axios
- **AI Algorithms**: Alpha-Beta Pruning (+ Node Reordering, Caching, and Evaluation Function), Minimax

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Abu-ls-10/checkers_ai
    cd checkers_ai
    ```

2. **Install backend dependencies**:
    Navigate to the `backend` folder:
    ```bash
    cd backend
    pip install flask
    pip install -U flask-cors
    ```

3. **Install frontend dependencies**:
    Navigate to the `frontend` folder:
    ```bash
    cd ../frontend
    npm install vite@latest
    ```

4. **Start the Flask server**:
    ```bash
    cd ../backend
    python app.py
    ```

5. **Start the React frontend**:
    In a new terminal window:
    ```bash
    cd ../frontend/ai-checkers-app
    npm run dev 
    ```
    OR
   ```bash
   npm start
   ```

## Usage

1. **Launch the Game**:
   Open a web browser and go to `http://localhost:XXXX` (`XXXX` is the port on which `ai-checkers-app` is hosted) to start the game.
   
2. **Gameplay**:
   - Select a piece to view available moves.
   - Click on a tile to move the selected piece.
   - Play turns against the AI until a win or stalemate is reached.

3. **Making Moves**:
   - The game alternates between the user and the AI after each move.
   - The **applyUserMove** API call applies user moves, while **fetchAIMove** retrieves AI moves.

## Game Rules

1. **Piece Movement**:
   - Pieces move diagonally on dark squares.
   - Kings can move both forward and backward.
   
2. **Capturing**:
   - Pieces can capture opponents by jumping over them.
   - Multiple jumps are allowed in a single turn if available.

3. **Winning Conditions**:
   - A player wins by capturing all opponent pieces or blocking them from making any legal moves.

## API Endpoints

- **`POST /user_move`**: Fetch available moves for the selected piece.
- **`POST /apply_user_move`**: Apply the user’s selected move and update the board state.
- **`POST /ai_move`**: Fetch and apply the AI’s optimal move based on the current board state.

## Future Improvements

- **Multiplayer Mode**: Implement online multiplayer functionality.
- **Improved UI Animations**: Add animations for piece movement and captures.
- **Leaderboard**: Track and display user wins against the AI.
