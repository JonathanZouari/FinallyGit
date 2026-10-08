# Tic-Tac-Toe

A command-line Tic-Tac-Toe game written in Python. Play against another person, or against a computer that never loses.

## Requirements

- Python 3.8 or newer
- No extra packages

## How to run

```bash
python Tictactoe.py
```

## How to play

1. Choose a mode:
   - `1` — two human players
   - `2` — play against the computer
2. Against the computer, choose `*` (you go first) or `#` (the computer goes first).
3. On your turn, type a square number from `1` to `9`. Empty squares show their numbers on the board.

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

The first player to get three marks in a row, column, or diagonal wins. If every square is filled and nobody has three in a row, the game is a draw. After each game you can play again.

## Computer opponent

The computer uses minimax to look at every possible move. It plays a perfect game, so the best you can do is a draw.
