# Tic-Tac-Toe

A terminal Tic-Tac-Toe game written in Python. Play against a friend or against the computer. The computer uses the minimax algorithm, so it plays optimally.

## Requirements

- Python 3

No extra packages are needed.

## How to run

From the project folder:

```bash
python Tictactoe.py
```

## How to play

1. Choose a mode:
   - `1` — two players on the same computer
   - `2` — play against the computer
2. If you play against the computer, choose `X` (goes first) or `O`.
3. On your turn, enter a square number from **1 to 9**.

The board is numbered like this:

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

The game ends when a player gets three in a row or the board is full (draw). You can start another round after that.

## Files

- `Tictactoe.py` — the full game (board, turns, win checks, and computer AI)
