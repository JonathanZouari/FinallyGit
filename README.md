# Tic-Tac-Toe

A command-line Tic-Tac-Toe game in Python. Play against a friend on the same keyboard, or against a computer opponent that never loses.

## Requirements

- Python 3.6 or newer
- No external packages

## How to run

```bash
python Tictactoe.py
```

## How to play

1. Choose a mode:
   - `1` — two players, taking turns at the same keyboard
   - `2` — play against the computer
2. Against the computer, choose whether to play as **X** (moves first) or **O**.
3. On your turn, enter a number from 1 to 9 to place your mark. Empty squares show their number:

   ```
   1 | 2 | 3
   --+---+--
   4 | 5 | 6
   --+---+--
   7 | 8 | 9
   ```

4. The first player to get three in a row (horizontally, vertically or diagonally) wins. If the board fills up with no winner, it's a draw.
5. After each game you can play again (`y`) or quit (`n`).

Invalid input — anything other than 1–9, or a square that's already taken — is rejected and you're asked again.

## How the computer plays

The computer uses the **minimax** algorithm: it explores every possible continuation of the game and picks the move with the best guaranteed outcome. Because Tic-Tac-Toe is small enough to search completely, the computer plays perfectly — the best you can do is a draw.

## Code overview

| Function | Purpose |
|---|---|
| `WIN_LINES` | The 8 winning combinations of board positions |
| `winner(board)` | Returns `"X"` or `"O"` if someone has won, otherwise `None` |
| `board_full(board)` | `True` when no empty squares remain |
| `print_board(board)` | Prints the board, numbering empty squares |
| `empty_cells(board)` | Lists the indices of empty squares |
| `minimax(board, mark, maximizing)` | Recursively scores moves: `1` win, `0` draw, `-1` loss |
| `computer_move(board, mark)` | Plays the move minimax chooses |
| `human_move(board, mark)` | Prompts for and validates a player's move |
| `play(vs_computer)` | Runs a single game |
| `main()` | Mode selection and the play-again loop |

The board is a list of 9 strings (`""`, `"X"` or `"O"`), indexed 0–8 internally and shown to the player as 1–9.