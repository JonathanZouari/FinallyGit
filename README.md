# Tic-Tac-Toe

A command-line Tic-Tac-Toe game written in Python. Play against a friend or against a computer opponent that uses the minimax algorithm (unbeatable with perfect play).

## Requirements

- Python 3

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

When the game starts, choose a mode:

1. **Two players** — take turns on the same keyboard.
2. **Vs computer** — play against the AI. You can choose **X** (goes first) or **O**.

The board is numbered **1–9**:

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

Enter a number to place your mark on that square. The game ends with a win or a draw, then you can choose to play again.

## Features

- Two-player and single-player modes
- Choice of X or O against the computer
- Input validation (range and occupied squares)
- Unbeatable computer using minimax
