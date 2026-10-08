# Tic-Tac-Toe

A command-line Tic-Tac-Toe game for two players or one player versus the computer.

The computer uses minimax, so it always plays optimally. You can draw against it, but you cannot beat it.

## Requirements

- Python 3 (standard library only)

## Run

```bash
python Tictactoe.py
```

## How to play

1. Choose a mode:
   - `1` — two human players
   - `2` — play against the computer
2. In computer mode, pick `X` (goes first) or `O`.
3. Enter a square number from **1** to **9**:

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

Occupied squares show `X` or `O` instead of a number. Invalid or taken squares are rejected and you are asked again.

The game ends on a win or a draw, then asks if you want to play again.
