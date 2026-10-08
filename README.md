# Tic-Tac-Toe

Classic Tic-Tac-Toe in Python. Play in the terminal or with a desktop GUI. Marks are `*` (first) and `#` (second).

## Features

- Terminal and GUI versions
- Two-player mode or vs computer
- Optimal minimax AI (never loses)
- Choose `*` or `#` when playing the computer
- New game / replay support

## Requirements

- Python 3.8+
- No third-party packages (`tkinter` is included with most Python installs)

## Quick start

**GUI (recommended):**

```bash
python TictactoeGUI.py
```

**Terminal:**

```bash
python Tictactoe.py
```

### GUI controls

1. Pick **vs Computer** or **Two Players**
2. In computer mode, choose your mark (`*` goes first)
3. Click a square to place your mark
4. Use **New Game** to restart

### Terminal controls

1. Choose `1` for two players, or `2` vs computer
2. In computer mode, pick `*` or `#`
3. Enter a square number (`1`–`9`)
4. Type `y` to play again

## Board layout

```
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

## Project layout

```
.
├── Tictactoe.py      # Shared logic + terminal game
├── TictactoeGUI.py   # Desktop GUI (tkinter)
└── README.md
```

## How it works

Win detection checks all eight lines (rows, columns, diagonals). Against the computer, moves are chosen with **minimax**, so perfect play from both sides always ends in a draw.
