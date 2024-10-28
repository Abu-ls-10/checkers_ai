import './App.css';

const App = () => {
  const boardSize = 8;

  // Define the board layout
  const boardLayout = [
    ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
    ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['r', '.', 'r', '.', 'r', '.', 'r', '.'],
    ['.', 'r', '.', 'r', '.', 'r', '.', 'r'],
    ['r', '.', 'r', '.', 'r', '.', 'r', '.']
  ];

  // Function to render each tile
  const renderTile = (row, col) => {
    const isLightBrown = (row + col) % 2 === 0; // Adjust condition for light brown
    const tileClass = isLightBrown ? 'tile beige' : 'tile brown'; // Switch colors
    const piece = boardLayout[row][col];

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
      <div className="game-info">
        <h1 style={{ fontSize: '2.5rem', marginBottom: '10px' }}>Welcome to Checkers AI!</h1>
        
        <p style={{ fontSize: '1.2rem', color: '#555' }}>
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

        {/* Optional Features */}
        <div style={{ marginTop: '20px' }}>
          <button style={{
            margin: '10px',
            padding: '10px 20px',
            fontSize: '1rem',
            backgroundColor: '#4CAF50',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}>
            New Game
          </button>
        </div>
      </div>
      <div className="app">
        <h2>Your Turn:</h2>
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
