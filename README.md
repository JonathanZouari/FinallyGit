# Tic-Tac-Toe

A command-line Tic-Tac-Toe game written in Python. Play against another person or against a computer opponent that uses minimax (it plays optimally).

## Requirements

- Python 3

## How to run

From the project directory:

```bash
python Tictactoe.py
```

On some systems you may need `python3` instead of `python`.

## How to play

1. Choose a mode:
   - **1** — two players on the same keyboard
   - **2** — play against the computer
2. Squares are numbered **1–9**, left to right, top to bottom:

   ```
   1 | 2 | 3
   --+---+--
   4 | 5 | 6
   --+---+--
   7 | 8 | 9
   ```

3. **X** always goes first. In vs-computer mode you can choose to play as **X** or **O**.
4. After a game ends, you can start another round or quit.

The computer never misses a winning move and never leaves you an unblocked win, so a perfect game from both sides ends in a draw.
