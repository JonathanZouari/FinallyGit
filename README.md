# Tic-Tac-Toe

A console Tic-Tac-Toe game written in Python. Play against another person or against the computer.

## Requirements

- Python 3

## Run

```bash
python Tictactoe.py
```

## How to play

At the start of each game, choose a mode:

1. **Two players** — you and another person take turns on the same keyboard. X always goes first.
2. **Vs computer** — play as X (goes first) or O. The computer uses minimax and plays a perfect game, so the best result against it is a draw.

Squares are numbered 1–9, left to right, top to bottom:

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

Empty squares show their number. Taken squares show `X` or `O`. Enter a number from 1 to 9 on your turn. After a win or a draw, you can play again or quit.
