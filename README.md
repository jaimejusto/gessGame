# gessGame
Gess is a two player game that is a combination of Chess and Go.

## Rules:
- Starting with Black, players take turns to move their piece on the board.
- A move must change the stone configuration, therefore, a player is not allowed to skip their turn. 
- A piece consists of a 3x3 grid of squares, called the footprint, which may only be moved by the player whose stones are within the 3x3 grid.
  - A piece cannot contain stones of the other player.
  - A piece must contain at least one stone around the central square.
- As a piece moves, all of the stones in its footprint move in unison.

- Each piece can move based on the arrangement of stones in its footprint:
  - If the center of the footprint is unoccupied, it may only move up to three spaces but if the center is occupied, it may move any number of spaces as long as there are no stones blocking its path.
  - The surrounding squares determine the direction the piece can move. If a square is occupied by a stone, the piece may move in the direction indicated by the square's location relative to the central square; if a square is unoccupied, the piece cannot move in that direction.
- When the footprint overlaps with any other stones on the board, those stones are removed from the board and the move ends.
- If the footprint moves partially out of the board, the move ends. The stones of the piece which are on the square that has moved out of the board are removed.
- A move may also end before any stone is removed.
- The objective of the game is to be the only player with a ring piece on the board. If a player has no ring pieces on the board after their turn, that player loses the game. If neither player has a ring piece, the player who has just moved loses the game.
- A ring is any piece consisting of eight stones around an empty central square. 
