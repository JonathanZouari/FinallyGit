# Tic-Tac-Toe

A terminal Tic-Tac-Toe game in Python. Play two players on the same keyboard, or against a computer that uses the Minimax algorithm.

## Requirements

- Python 3

No extra packages are needed.

## Run

From the project folder:

```bash
python Tictactoe.py
```

On Windows you can also use:

```bash
py Tictactoe.py
```

## How to play

1. Choose a mode:
   - `1` — two players (X and O)
   - `2` — vs computer
2. Against the computer, choose whether to play as X (goes first) or O.
3. On each turn, enter a number from `1` to `9` for the square:

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

The game ends with a win (row, column, or diagonal) or a draw. After each round you can play again.

## Files

- `Tictactoe.py` — board, input, win checks, and computer moves.
