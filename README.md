# Tic-Tac-Toe

A command-line Tic-Tac-Toe game written in Python. Play against a friend on the same keyboard, or against a computer opponent that uses minimax and never loses.

## Requirements

- Python 3

## How to run

From the project folder:

```bash
python Tictactoe.py
```

On some systems you may need `python3` instead of `python`.

## How to play

When the game starts, choose a mode:

1. **Two players** — X and O take turns on the same computer.
2. **Vs computer** — play against the AI. You can choose to be X (goes first) or O.

The board is numbered 1–9:

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

Enter a number from 1 to 9 to place your mark. Occupied squares are rejected. The first player to get three in a row (horizontally, vertically, or diagonally) wins. If the board fills with no winner, the game is a draw.

After each game you can play again or quit.
