# Tic-Tac-Toe

A command-line Tic-Tac-Toe game written in Python. Play against a friend on the same computer, or against a computer opponent that uses the minimax algorithm.

## Requirements

- Python 3.7 or later

No extra packages are needed.

## How to run

From the project folder:

```bash
python Tictactoe.py
```

On some systems you may need:

```bash
python3 Tictactoe.py
```

## How to play

1. Choose a mode:
   - **1** — two players (X and O take turns on the same keyboard)
   - **2** — play against the computer
2. If you play against the computer, pick **X** (you go first) or **O** (the computer goes first).
3. Enter a number from **1** to **9** to place your mark:

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

The game ends when someone gets three in a row, or when the board is full (draw). You can start another round after each game.

## Features

- Two-player hot-seat mode
- Single-player mode vs an unbeatable computer (minimax)
- Input checks for invalid or already taken squares
- Option to play again without restarting the program
