# Tic-Tac-Toe

A Python Tkinter tic-tac-toe game. Play two players on the same computer, or against a computer opponent that uses minimax.

Marks on the board are `*` (first) and `#` (second).

## Requirements

- Python 3
- Tkinter (usually included with Python on Windows)

## Run

```bash
python Tictactoe.py
```

## How to play

- **Two players** — two people take turns on the same board. `*` always goes first.
- **Vs computer** — play against the computer. Choose `*` or `#`. If you pick `#`, the computer moves first.
- Click an empty cell to place the current mark.
- A winning line is highlighted in green. A tie shows `Draw.`
- **New game** resets the board. Changing mode or mark also starts a new game.

## Layout

| File | Role |
|------|------|
| `Tictactoe.py` | UI, win logic, and minimax for the computer opponent |
