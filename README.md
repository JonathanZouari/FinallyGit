# Tic-Tac-Toe

Classic Tic-Tac-Toe in the terminal. Play hot-seat with a friend, or challenge a computer that never loses.

## Features

- Two-player mode on the same keyboard
- Single-player mode with an optimal minimax AI
- Choose X (first) or O when playing the computer
- Clear board display with numbered empty squares
- Replay loop until you quit

## Requirements

- Python 3.8+
- No third-party packages

## Quick start

```bash
python Tictactoe.py
```

When prompted:

1. Choose `1` for two players, or `2` to play against the computer
2. In computer mode, pick `X` or `O`
3. Enter a square number (`1`–`9`) on your turn
4. After the game ends, type `y` to play again or anything else to quit

## Board layout

Empty squares show their number. Marks replace the number when played:

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

## Project layout

```
.
├── Tictactoe.py   # Game logic and CLI
└── README.md
```

## How it works

Win detection checks all eight lines (rows, columns, diagonals). Against the computer, moves are chosen with **minimax**, so perfect play from both sides always ends in a draw.
