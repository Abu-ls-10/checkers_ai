import './App.css';
import { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const boardSize = 8;

  // Define initial board layout and state
  const initialBoard = [
    ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
    ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['r', '.', 'r', '.', 'r', '.', 'r', '.'],
    ['.', 'r', '.', 'r', '.', 'r', '.', 'r'],
    ['r', '.', 'r', '.', 'r', '.', 'r', '.']
  ];
  const [board, setBoard] = useState(initialBoard);
  const [selectedPiece, setSelectedPiece] = useState(null);
  // const [selectedCell, setSelectedCell] = useState(null);
  const [availableMoves, setAvailableMoves] = useState({"5,4": [[4, 5]]});
  // const [aiMove, setAIMove] = useState([]);
  const [isUserTurn, setIsUserTurn] = useState(true);
  const [numRed, setNumRed] = useState(12)
  const [numBlack, setNumBlack] = useState(12)



  // Fetch available moves for the selected piece
  const fetchAvailableMoves = async () => {
    try {
      const response = await axios.post('http://localhost:5000/user_move');
      setAvailableMoves(response.data.user_moves);
    } catch (error) {
      console.error("Error fetching available moves:", error);
    }
  };

  // Fetch AI's move from Flask and apply it
  const fetchAIMove = async () => {
    try {
      const response = await axios.post('http://localhost:5000/ai_move');
      // setAIMove(response.data.ai_move);
      setBoard(response.data.board_state);
      setNumRed(response.data.num_red);
      setNumBlack(response.data.num_black);
      // setIsUserTurn(true)
    } catch (error) {
      console.error("Error fetching AI move:", error);
    }
  };

  // Game loop execution
  useEffect(() => {

    // Handle cell click to select/move pieces, returns true if move is completed
    const handleCellClick = async (row, col) => {
      // Format the coordinates as strings to match availableMoves keys
      const pieceKey = `${row},${col}`;

      // Check if the clicked cell contains a red piece (user's turn)
      if (board[row][col] === 'r' || board[row][col] === 'R') {
        // Check if the piece at (row, col) has available moves
        if (availableMoves && Object.prototype.hasOwnProperty.call(availableMoves, pieceKey)) {
          setSelectedPiece([row, col]);
          return false; // Piece selection only, no move completed yet
        }
      } else if (board[row][col] === '.' && selectedPiece) {
        const [selectedRow, selectedCol] = selectedPiece;
        const selectedPieceKey = `${selectedRow},${selectedCol}`;

        // Check if the selected piece has a valid move to the clicked cell
        if (
          availableMoves[selectedPieceKey]?.some(
            (move) => move[0] === row && move[1] === col
          )
        ) {
          await applyUserMove([selectedRow, selectedCol], [row, col]);
          setSelectedPiece(null); // Reset selected piece after move
          return true; // Move completed
        }
      }

      return false; // No move completed
    };


    // Apply user's move via Flask
    const applyUserMove = async (oldCoords, newCoords) => {
      try {
        const response = await axios.post('http://localhost:5000/apply_user_move', {
          old_coords: oldCoords,
          new_coords: newCoords,
          piece: board[oldCoords[0]][oldCoords[1]],
        });
        setBoard(response.data.board_state);
        setNumRed(response.data.num_red);
        setNumBlack(response.data.num_black);
        // setIsUserTurn(false)
      } catch (error) {
        console.error("Error applying user move:", error);
      }
    };

    const playGame = async () => {

      // Main game loop that runs until no available moves or game is over
      while (Object.keys(availableMoves).length !== 0 && numRed > 0 && numBlack > 0) {
        if (isUserTurn) {
          await fetchAvailableMoves();
          console.log("Checking pos:");

          const captureUserMove = new Promise((resolve) => {
            // Handle user's multiple clicks to select piece and move
            const handleUserClick = (e) => {
              const pos = e.target.closest('.tile, .piece');
              if (!pos) return; // Ignore clicks outside of tiles and pieces

              console.log("Checking pos:")
              const row = parseInt(pos.dataset.row);
              const col = parseInt(pos.dataset.col);

              handleCellClick(row, col).then((moveCompleted) => {
                if (moveCompleted) {
                  // Stop listening for clicks once a valid move is made
                  document.removeEventListener('click', handleUserClick);
                  resolve(); // Resolve to continue game loop
                }
              });
            };

            // Add event listener for clicks on board
            document.addEventListener('click', handleUserClick);
          });

          await captureUserMove;  // Wait for user to complete a valid move
          setIsUserTurn(false);   // Switch turn to AI
        } else {
          await fetchAIMove();
          setIsUserTurn(true); // Switch back to user turn
        }
      }
    };

    playGame();
  }, []);

  // Render each tile with optional highlighting
  const renderTile = (row, col) => {
    const isLight = (row + col) % 2 === 0;
    const tileClass = isLight ? 'tile light' : 'tile dark';
    const piece = board[row][col];
    // const isSelected = selectedPiece && selectedPiece[0] === row && selectedPiece[1] === col;
    // const isAvailableMove = availableMoves.some(
    //   (move) => move[0] === row && move[1] === col
    // );

    return (
      <div key={`${row}-${col}`} className={tileClass}>
        {piece === 'b' && <div className={'piece black'}></div>}
        {piece === 'r' && <div className={'piece red'}></div>}
        {piece === 'B' && <div className={'piece black-king'}></div>}
        {piece === 'R' && <div className={'piece red-king'}></div>}
      </div>
    );
  };
  

  return (
    <div className='main-display'>

      {/* Game Info */}
      <div className="game-info">
        <h1 style={{ fontSize: '2.5rem', marginBottom: '10px' }}>Welcome to Checkers AI!</h1>
        
        <p style={{ fontSize: '1.2rem', color: '#b3b3b3' }}>
          Challenge the AI in a strategic game of checkers. Outsmart the computer, or hone your skills
          against a formidable opponent. Ready to play?
        </p>

        {/* Instructions */}
        <h3>How to Play</h3>
        <ol style={{padding: '0px 0px 0px 30px' }}>
          <li>Click on a piece to select it.</li>
          <li>Available moves will be highlighted.</li>
          <li>Make your move and challenge the AI!</li>
        </ol>

        {/* Rules */}
        <h3>Checkers Rules</h3>
        <ul style={{padding: '0px 0px 0px 30px' }}>
          <li><strong>Starting Position:</strong> Each player begins with 12 pieces on dark squares closest to their side.</li>
          <li><strong>Moves:</strong>
            <ul>
              <li><strong>Simple Move:</strong> Move one square diagonally forward to an empty dark square (kings can move in any diagonal direction).</li>
              <li><strong>Jump:</strong> Capture an opponent&apos;s piece by jumping over it to an empty square. Multiple jumps are required if available. Jumping is mandatory if possible.</li>
            </ul>
          </li>
          <li><strong>Kings:</strong> Pieces reaching the last row are crowned as kings, allowing movement in any diagonal direction.</li>
          <li><strong>Winning:</strong> Capture all opponent pieces or leave them with no moves.</li>
        </ul>

        {/* New Game Button */}
        <div style={{ marginTop: '20px' }}>
          <button className='button'>Start New Game</button>
        </div>
      </div>

      {/* Game App (Checkers) */}
      <div className="app">
        <h2>{isUserTurn ? "Your Turn" : "AI's Turn"}</h2>

        <div className="board">
          {Array.from({ length: boardSize }).map((_, row) =>
            Array.from({ length: boardSize }).map((_, col) => renderTile(row, col))
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
