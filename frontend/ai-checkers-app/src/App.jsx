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
  const [availableMoves, setAvailableMoves] = useState({
    "5,0": [[4, 1]], "5,2": [[4, 1], [4, 3]], 
    "5,4": [[4, 3], [4, 5]], "5,6": [[4, 5], [4, 7]]
  });
  // const [aiMove, setAIMove] = useState([]);
  const [isUserTurn, setIsUserTurn] = useState(true);
  // const [moveApplied, setMoveApplied] = useState(false);
  const [numRed, setNumRed] = useState(12);
  const [numBlack, setNumBlack] = useState(12);



  // Fetch available moves for the selected piece
  const fetchAvailableMoves = async () => {
    try {
      const response = await axios.post('http://localhost:5000/user_move');
      setAvailableMoves(response.data.user_moves);
      console.log(availableMoves);
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

  // Apply user's move via Flask
  const applyUserMove = async (oldCoords, newCoords) => {
    if (!isUserTurn) return;
    try {
      const response = await axios.post('http://localhost:5000/apply_user_move', {
        old_coords: oldCoords,
        new_coords: newCoords,
        piece: board[oldCoords[0]][oldCoords[1]],
      });
      setBoard(response.data.board_state);
      setNumRed(response.data.num_red);
      setNumBlack(response.data.num_black);
      setIsUserTurn(false)
    } catch (error) {
      console.error("Error applying user move:", error);
    }
  };

  // Handle cell click to select/move pieces, returns true if move is completed
  const handleCellClick = async (row, col) => {
    // Format the coordinates as strings to match availableMoves keys
    const pieceKey = `${row},${col}`;

    console.log(row, col);
    console.log(selectedPiece);

    // Check if the clicked cell contains a red piece (user's turn)
    if (board[row][col] === 'r' || board[row][col] === 'R') {
      // Check if the piece at (row, col) has available moves
      console.log("Red piece selected");
      if (availableMoves && Object.prototype.hasOwnProperty.call(availableMoves, pieceKey)) {
        setSelectedPiece([row, col]);
        console.log("Piece can Move!");
        return false; // Piece selection only, no move completed yet
      }
    } else if (board[row][col] === '.' && selectedPiece !== null) {
      const [selectedRow, selectedCol] = selectedPiece;
      const selectedPieceKey = `${selectedRow},${selectedCol}`;
      console.log("Selected a tile after selecting a piece");

      // Check if the selected piece has a valid move to the clicked cell
      if (
        availableMoves[selectedPieceKey]?.some(
          (move) => move[0] === row && move[1] === col
        )
      ) {
        console.log("Can move to this tile!");
        await applyUserMove([selectedRow, selectedCol], [row, col]);
        console.log("board:", board);

        setSelectedPiece(null); // Reset selected piece after move
        return true; // Move completed
      }
    }

    return false; // No move completed
  };

  let listenerCount = 0; // Initialize a counter for event listeners

  // Function to handle the user's turn
  const handleUserTurn = async () => {
    if (listenerCount > 0) return;
    const captureUserMove = new Promise((resolve) => {
      const handleUserClick = (e) => {
        const pos = e.target.closest('.tile, .piece.red, .piece.red-king');
        if (!pos) return;

        const row = parseInt(pos.dataset.row);
        const col = parseInt(pos.dataset.col);

        handleCellClick(row, col).then((moveCompleted) => {
          console.log("MOVE STATUS:", moveCompleted);
          if (moveCompleted) {
            document.removeEventListener('click', handleUserClick); // Remove listener after move
            listenerCount--; // Decrement the listener count
            resolve(); // Resolve the promise once the move is made
          }
        });
      };

      document.addEventListener('click', handleUserClick); // Add new listener
      listenerCount++; // Increment the listener count
      console.log(`Listeners added: ${listenerCount}`);
    });

    await captureUserMove; // Wait for a valid move
  };

  // useEffect to initiate the game loop
  useEffect(() => {
    const playGame = async () => {
      // Main game loop
      if (availableMoves.length !== 0 && numRed > 0 && numBlack > 0) {
        if (isUserTurn) {
          await handleUserTurn();
          setIsUserTurn(false);
        } else {
          await fetchAIMove();
          setIsUserTurn(true);  // Switch back to user turn after AI move
          console.log("CALLED FETCH_AVAILABLE_MOVES()");
          await fetchAvailableMoves();
        }
      }
    };

    playGame();
    console.log("USE_EFFECT triggered. Current board:", board, "Available moves:", availableMoves);
    console.log(`Current listener count: ${listenerCount}`);
  }, [board, isUserTurn, selectedPiece, availableMoves, numBlack, numRed]);


  // Render each tile with optional highlighting
  const renderTile = (row, col) => {
    console.log("Inside renderTile");
    const isLight = (row + col) % 2 === 0;
    const tileClass = isLight ? 'tile light' : 'tile dark';
    const piece = board[row][col];
    // const isSelected = selectedPiece && selectedPiece[0] === row && selectedPiece[1] === col;
    // const isAvailableMove = availableMoves.some(
    //   (move) => move[0] === row && move[1] === col
    // );

    return (
      <div key={`${row}-${col}`} className={tileClass} data-row={row} data-col={col}>
        {piece === 'b' && <div className={'piece black'} data-row={row} data-col={col}></div>}
        {piece === 'r' && <div className={'piece red'} data-row={row} data-col={col}></div>}
        {piece === 'B' && <div className={'piece black-king'} data-row={row} data-col={col}></div>}
        {piece === 'R' && <div className={'piece red-king'} data-row={row} data-col={col}></div>}
      </div>
    );
  };
  

  return (
    <div className='main-display'>

      {/* Game Info */}
      <div className="game-info">
        <h1 style={{ fontSize: '2.5rem', marginBottom: '10px' }}>Welcome to Checkers&nbsp;AI!</h1>
        
        <p style={{ fontSize: '1.2rem', color: '#b3b3b3' }}>
          Challenge the AI in a strategic game of checkers. Outsmart the computer, or hone your skills
          against a formidable opponent. Ready to play?
        </p>

        {/* Instructions */}
        <h3>How&nbsp;to&nbsp;Play</h3>
        <ol style={{padding: '0px 0px 0px 30px' }}>
          <li>Click on a piece to select it.</li>
          <li>Available moves will be highlighted.</li>
          <li>Make your move and challenge the AI!</li>
        </ol>

        {/* Rules */}
        <h3>Checkers&nbsp;Rules</h3>
        <ul style={{padding: '0px 0px 0px 30px' }}>
          <li><strong>Starting Position:</strong> Each player begins with 12 pieces on dark squares closest to their side.</li>
          <li><strong>Moves:</strong>
            <ul>
              <li><strong>Simple&nbsp;Move:</strong> Move one square diagonally forward to an empty dark square (kings can move in any diagonal direction).</li>
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
