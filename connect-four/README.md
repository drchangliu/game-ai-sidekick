# Connect Four
Connect Four is a game in which the players choose a color and then take turns dropping colored tokens into a six-row, seven-column vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own tokens.

[Connect Four Wikipedia](https://en.wikipedia.org/wiki/Connect_Four)

# Related Prompts
## Rules Prompt
```plaintext
Game Rules:
Two players, Player 1 and Player 2, take turns making one move per turn. The game is played on a 6 tall, 7 wide grid, where players place pieces in columns. Players alternate turns, and the goal is to be the first to create a sequence of four of their pieces in a row, column, or diagonal.
On a turn, a player must:
- Place a piece: Select a column (1-7) to place their piece. The piece will fall to the lowest available space in that column.
The game ends when a player creates a sequence of four of their pieces in a row, column, or diagonal. That player wins. If the grid is completely filled, and no player has created a sequence of four. In this case, the game is a draw.

Game State Format:
Game states are represented as a grid of 0, 1, and 2's. For example, [0000000;0000000;0001000;0002000;0012000;0121000;], where `0` represents an empty space, `1` represents Player 1's pieces, and `2` represents Player 2's pieces.

Move Format:
Moves are represented as a single number, corresponding to the column (1-7) where the player places their piece.
```

## Game Aware Prompt
```plaintext
You are playing Connect Four.

Game State Format:
Game states are represented as a grid of 0, 1, and 2's. For example, [0000000;0000000;0001000;0002000;0012000;0121000;], where `0` represents an empty space, `1` represents Player 1's pieces, and `2` represents Player 2's pieces.

Move Format:
Moves are represented as a single number, corresponding to the column (1-7) where the player places their piece.
```

## One-Step Game State Prompt
```plaintext
You are Player 1.
It's your turn.
The current game state is [0202200;0101100;0101100;0201100;0122202;2211202].
What is the best move?
```

### Correct Response
```plaintext
Move: 3
Resulting State: [0202200;0101100;0101100;0211100;0122202;2211202] (game over)
```
