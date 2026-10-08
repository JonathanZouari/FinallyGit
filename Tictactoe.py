"""Tic-Tac-Toe. Run: python Tictactoe.py"""

import tkinter as tk

FIRST = "*"
SECOND = "#"

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


def winner(board):
    for line in WIN_LINES:
        a, b, c = line
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], line
    return None, ()


def board_full(board):
    return all(board)


def empty_cells(board):
    return [index for index, cell in enumerate(board) if not cell]


def other(mark):
    return SECOND if mark == FIRST else FIRST


def minimax(board, mark, maximizing):
    found, _ = winner(board)
    if found == mark:
        return 1, None
    if found:
        return -1, None
    if board_full(board):
        return 0, None

    opponent = other(mark)
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


def best_move(board, mark):
    _, index = minimax(board, mark, True)
    return index


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f5")

        self.board = [""] * 9
        self.buttons = []
        self.turn = FIRST
        self.vs_computer = False
        self.human_mark = FIRST
        self.game_over = False
        self._computer_job = None

        self._build()
        self.new_game()

    def _build(self):
        outer = tk.Frame(self.root, bg="#f4f4f5", padx=16, pady=16)
        outer.pack()

        tk.Label(
            outer,
            text="Tic-Tac-Toe",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f4f5",
            fg="#18181b",
        ).pack(pady=(0, 12))

        modes = tk.Frame(outer, bg="#f4f4f5")
        modes.pack()
        self.mode_var = tk.StringVar(value="players")
        tk.Radiobutton(
            modes,
            text="Two players",
            variable=self.mode_var,
            value="players",
            command=self._on_mode_change,
            bg="#f4f4f5",
            activebackground="#f4f4f5",
            font=("Segoe UI", 11),
        ).pack(side="left", padx=8)
        tk.Radiobutton(
            modes,
            text="Vs computer",
            variable=self.mode_var,
            value="computer",
            command=self._on_mode_change,
            bg="#f4f4f5",
            activebackground="#f4f4f5",
            font=("Segoe UI", 11),
        ).pack(side="left", padx=8)

        self.mark_frame = tk.Frame(outer, bg="#f4f4f5")
        self.mark_frame.pack(pady=(8, 0))
        tk.Label(
            self.mark_frame,
            text="You play as",
            bg="#f4f4f5",
            font=("Segoe UI", 11),
        ).pack(side="left")
        self.mark_var = tk.StringVar(value=FIRST)
        for mark in (FIRST, SECOND):
            tk.Radiobutton(
                self.mark_frame,
                text=mark,
                variable=self.mark_var,
                value=mark,
                command=self._on_mark_change,
                bg="#f4f4f5",
                activebackground="#f4f4f5",
                font=("Segoe UI", 12, "bold"),
            ).pack(side="left", padx=6)

        self.status = tk.Label(
            outer,
            text="",
            font=("Segoe UI", 13),
            bg="#f4f4f5",
            fg="#3f3f46",
            pady=10,
        )
        self.status.pack()

        grid = tk.Frame(outer, bg="#d4d4d8")
        grid.pack()
        for index in range(9):
            button = tk.Button(
                grid,
                text="",
                width=4,
                height=2,
                font=("Segoe UI", 22, "bold"),
                bg="white",
                activebackground="#e4e4e7",
                relief="flat",
                command=lambda i=index: self.on_click(i),
            )
            button.grid(row=index // 3, column=index % 3, padx=2, pady=2)
            self.buttons.append(button)

        tk.Button(
            outer,
            text="New game",
            font=("Segoe UI", 11),
            command=self.new_game,
            padx=12,
            pady=4,
        ).pack(pady=(14, 0))

    def _on_mode_change(self):
        self.new_game()

    def _on_mark_change(self):
        if self.vs_computer:
            self.new_game()

    def _cancel_computer(self):
        if self._computer_job is not None:
            self.root.after_cancel(self._computer_job)
            self._computer_job = None

    def new_game(self):
        self._cancel_computer()
        self.board = [""] * 9
        self.turn = FIRST
        self.game_over = False
        self.vs_computer = self.mode_var.get() == "computer"
        self.human_mark = self.mark_var.get() if self.vs_computer else FIRST
        if self.vs_computer:
            self.mark_frame.pack(pady=(8, 0), before=self.status)
        else:
            self.mark_frame.pack_forget()
        for button in self.buttons:
            button.config(text="", fg="#18181b", bg="white")
        self._refresh_status()
        if self.vs_computer and self.turn != self.human_mark:
            self._schedule_computer()

    def on_click(self, index):
        if self.game_over or self.board[index]:
            return
        if self.vs_computer and self.turn != self.human_mark:
            return
        self._place(index)
        if not self.game_over and self.vs_computer:
            self._schedule_computer()

    def _schedule_computer(self):
        self.status.config(text="Computer is thinking...")
        self._computer_job = self.root.after(250, self._computer_turn)

    def _computer_turn(self):
        self._computer_job = None
        if self.game_over or self.turn == self.human_mark:
            return
        self._place(best_move(self.board, self.turn))

    def _place(self, index):
        mark = self.turn
        self.board[index] = mark
        color = "#2563eb" if mark == FIRST else "#be123c"
        self.buttons[index].config(text=mark, fg=color)
        found, line = winner(self.board)
        if found:
            self.game_over = True
            for cell in line:
                self.buttons[cell].config(bg="#bbf7d0")
            self.status.config(text=f"{found} wins!")
            return
        if board_full(self.board):
            self.game_over = True
            self.status.config(text="Draw.")
            return
        self.turn = other(self.turn)
        self._refresh_status()

    def _refresh_status(self):
        if self.vs_computer and self.turn != self.human_mark:
            self.status.config(text="Computer's turn")
            return
        self.status.config(text=f"{self.turn}'s turn")


def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

print("adar")
