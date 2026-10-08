# Tic-Tac-Toe

A command-line Tic-Tac-Toe game written in Python. Play against another person or against a computer opponent that uses minimax and never loses.

## Requirements

- Python 3

No third-party packages are required.

## Run

```bash
python Tictactoe.py
```

## How to play

1. Choose a mode:
   - `1` — two players, taking turns in the terminal
   - `2` — you against the computer
2. Against the computer, choose `X` (you go first) or `O` (the computer goes first).
3. Enter a square number from `1` to `9`. Empty squares show their numbers; taken squares show `X` or `O`.

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

The game ends when a player gets three in a row (row, column, or diagonal) or when the board is full (a draw). After each game you can play again or quit.
