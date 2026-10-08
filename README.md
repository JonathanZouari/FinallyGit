# Tic-Tac-Toe

A command-line Tic-Tac-Toe game written in Python. Play against a friend on the same keyboard, or against a computer opponent that uses minimax.

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

Then choose a variant:

1. **Classic** — standard Tic-Tac-Toe. Marks stay on the board. The computer never loses.
2. **Infinite** — each player may keep only three marks. Placing a fourth mark removes that player's oldest mark. The board never fills, draws from a full board do not happen, and late-game positions stay interesting. When a player already has three marks, the game shows which square will vanish on their next move.

The board is numbered 1–9:

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

Enter a number from 1 to 9 to place your mark. Occupied squares are rejected. The first player to get three in a row (horizontally, vertically, or diagonally) wins. In classic mode, if the board fills with no winner, the game is a draw.

After each game you can play again or quit.
