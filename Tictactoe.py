"""Star vs Hash (tic-tac-toe). Run: python Tictactoe.py"""

import tkinter as tk
from tkinter import ttk

STAR = "*"
HASH = "#"

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

BG = "#1b1f2a"
PANEL = "#252b3a"
CELL = "#2f3648"
CELL_HOVER = "#3b445c"
WIN_CELL = "#2d6a4f"
STAR_COLOR = "#f4d35e"
HASH_COLOR = "#7eb8da"
TEXT = "#e8ecf4"
MUTED = "#9aa3b5"


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def winning_line(board):
    for line in WIN_LINES:
        a, b, c = line
        if board[a] and board[a] == board[b] == board[c]:
            return line
    return None


def board_full(board):
    return all(board)


def empty_cells(board):
    return [index for index, cell in enumerate(board) if not cell]


def minimax(board, mark, maximizing):
    found = winner(board)
    if found == mark:
        return 1, None
    if found:
        return -1, None
    if board_full(board):
        return 0, None

    opponent = HASH if mark == STAR else STAR
    current = mark if maximizing else opponent
    best_score = -2 if maximizing else 2
    best_move = None

    for index in empty_cells(board):
        board[index] = current
        score, _ = minimax(board, mark, not maximizing)
        board[index] = ""
        if maximizing and score > best_score:
            best_score, best_move = score, index
        elif not maximizing and score < best_score:
            best_score, best_move = score, index

    return best_score, best_move


def best_computer_move(board, mark):
    _, index = minimax(board, mark, True)
    return index


class StarHashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Star vs Hash")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.board = [""] * 9
        self.turn = STAR
        self.vs_computer = False
        self.human_mark = STAR
        self.computer_mark = HASH
        self.game_over = False
        self.busy = False
        self.cells = []

        self.mode_var = tk.StringVar(value="two")
        self.mark_var = tk.StringVar(value=STAR)

        self._build()
        self._new_game()

    def _build(self):
        pad = {"padx": 16, "pady": (16, 8)}

        title = tk.Label(
            self.root,
            text="Star vs Hash",
            font=("Segoe UI", 22, "bold"),
            fg=TEXT,
            bg=BG,
        )
        title.pack(**pad)

        controls = tk.Frame(self.root, bg=PANEL, padx=12, pady=12)
        controls.pack(fill="x", padx=16)

        tk.Label(controls, text="Mode", fg=MUTED, bg=PANEL, font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Radiobutton(
            controls, text="Two players", variable=self.mode_var, value="two"
        ).grid(row=1, column=0, sticky="w", padx=(0, 16))
        ttk.Radiobutton(
            controls, text="Vs computer", variable=self.mode_var, value="cpu"
        ).grid(row=1, column=1, sticky="w")

        tk.Label(
            controls, text="Your mark (vs computer)", fg=MUTED, bg=PANEL, font=("Segoe UI", 10)
        ).grid(row=2, column=0, sticky="w", pady=(8, 0), columnspan=2)
        ttk.Radiobutton(
            controls, text="* goes first", variable=self.mark_var, value=STAR
        ).grid(row=3, column=0, sticky="w", padx=(0, 16))
        ttk.Radiobutton(
            controls, text="# goes second", variable=self.mark_var, value=HASH
        ).grid(row=3, column=1, sticky="w")

        ttk.Button(controls, text="New game", command=self._new_game).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0)
        )

        board_frame = tk.Frame(self.root, bg=BG, padx=16, pady=16)
        board_frame.pack()

        for index in range(9):
            row, col = divmod(index, 3)
            button = tk.Button(
                board_frame,
                text="",
                font=("Segoe UI", 28, "bold"),
                width=4,
                height=2,
                bg=CELL,
                fg=TEXT,
                activebackground=CELL_HOVER,
                activeforeground=TEXT,
                relief="flat",
                bd=0,
                command=lambda i=index: self._on_click(i),
            )
            button.grid(row=row, column=col, padx=4, pady=4)
            self.cells.append(button)

        self.status = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 12),
            fg=TEXT,
            bg=BG,
        )
        self.status.pack(pady=(0, 16))

    def _new_game(self):
        self.board = [""] * 9
        self.turn = STAR
        self.vs_computer = self.mode_var.get() == "cpu"
        self.human_mark = self.mark_var.get() if self.vs_computer else STAR
        self.computer_mark = HASH if self.human_mark == STAR else STAR
        self.game_over = False
        self.busy = False
        for cell in self.cells:
            cell.config(text="", fg=TEXT, bg=CELL, state="normal")
        self._set_status(self._turn_message())
        if self.vs_computer and self.turn == self.computer_mark:
            self._schedule_computer()

    def _turn_message(self):
        if self.vs_computer:
            if self.turn == self.human_mark:
                return f"Your turn ({self.human_mark})"
            return f"Computer thinking ({self.computer_mark})..."
        return f"{self.turn}'s turn"

    def _set_status(self, text):
        self.status.config(text=text)

    def _on_click(self, index):
        if self.game_over or self.busy or self.board[index]:
            return
        if self.vs_computer and self.turn != self.human_mark:
            return
        self._place(index, self.turn)
        if not self.game_over:
            self._advance_turn()

    def _place(self, index, mark):
        self.board[index] = mark
        color = STAR_COLOR if mark == STAR else HASH_COLOR
        self.cells[index].config(text=mark, fg=color)
        found = winner(self.board)
        if found:
            self.game_over = True
            for i in winning_line(self.board):
                self.cells[i].config(bg=WIN_CELL)
            if self.vs_computer:
                if found == self.human_mark:
                    self._set_status(f"You win ({found})!")
                else:
                    self._set_status(f"Computer wins ({found})!")
            else:
                self._set_status(f"{found} wins!")
            return
        if board_full(self.board):
            self.game_over = True
            self._set_status("Draw.")

    def _advance_turn(self):
        self.turn = HASH if self.turn == STAR else STAR
        self._set_status(self._turn_message())
        if self.vs_computer and self.turn == self.computer_mark:
            self._schedule_computer()

    def _schedule_computer(self):
        self.busy = True
        self.root.after(350, self._computer_turn)

    def _computer_turn(self):
        if self.game_over:
            self.busy = False
            return
        index = best_computer_move(self.board, self.computer_mark)
        self.busy = False
        if index is None:
            return
        self._place(index, self.computer_mark)
        if not self.game_over:
            self._advance_turn()


def main():
    root = tk.Tk()
    StarHashApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
