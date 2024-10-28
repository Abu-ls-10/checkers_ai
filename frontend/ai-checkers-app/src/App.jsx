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
    <div className="app">
      <h1>AI Checkers</h1>
      <div className="board">
        {Array.from({ length: boardSize }).map((_, row) =>
          Array.from({ length: boardSize }).map((_, col) => renderTile(row, col))
        )}
      </div>
    </div>
  );
};

export default App;
