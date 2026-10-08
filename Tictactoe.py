"""Tic-Tac-Toe with a visual window. Run: python Tictactoe.py"""

import tkinter as tk
from tkinter import font as tkfont

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

BG = "#1a1d27"
PANEL = "#252a38"
LINE = "#3d4458"
TEXT = "#e8eaf0"
MUTED = "#9aa3b8"
X_COLOR = "#7ee0c8"
O_COLOR = "#f0a06a"
WIN_BG = "#2f4a42"
BTN = "#3a6ff0"
BTN_HOVER = "#5483ff"


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)
    return None, None


def board_full(board):
    return all(board)


def empty_cells(board):
    return [index for index, cell in enumerate(board) if not cell]


def minimax(board, mark, maximizing):
    found, _ = winner(board)
    if found == mark:
        return 1, None
    if found:
        return -1, None
    if board_full(board):
        return 0, None

    opponent = "O" if mark == "X" else "X"
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


def computer_move(board, mark):
    _, index = minimax(board, mark, True)
    return index


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.board = [""] * 9
        self.buttons = []
        self.vs_computer = True
        self.human_mark = "X"
        self.computer_mark = "O"
        self.turn = "X"
        self.game_over = False

        self.title_font = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.status_font = tkfont.Font(family="Segoe UI", size=12)
        self.cell_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.small_font = tkfont.Font(family="Segoe UI", size=10)

        self._build()
        self.new_game()

    def _build(self):
        pad = {"padx": 16, "pady": 8}

        tk.Label(
            self.root,
            text="Tic-Tac-Toe",
            font=self.title_font,
            fg=TEXT,
            bg=BG,
        ).pack(**pad)

        controls = tk.Frame(self.root, bg=BG)
        controls.pack(fill="x", padx=16)

        self.mode_var = tk.StringVar(value="computer")
        self._radio(controls, "Vs computer", "computer").pack(side="left", padx=(0, 12))
        self._radio(controls, "Two players", "human").pack(side="left")

        mark_row = tk.Frame(self.root, bg=BG)
        mark_row.pack(fill="x", padx=16, pady=(4, 0))
        tk.Label(
            mark_row,
            text="You play as:",
            font=self.small_font,
            fg=MUTED,
            bg=BG,
        ).pack(side="left", padx=(0, 8))
        self.mark_var = tk.StringVar(value="X")
        self._radio(mark_row, "X (first)", "X").pack(side="left", padx=(0, 8))
        self._radio(mark_row, "O (second)", "O").pack(side="left")

        self.status = tk.Label(
            self.root,
            text="",
            font=self.status_font,
            fg=TEXT,
            bg=BG,
        )
        self.status.pack(pady=(12, 4))

        board_frame = tk.Frame(self.root, bg=LINE, padx=4, pady=4)
        board_frame.pack(padx=16, pady=8)

        for index in range(9):
            row, col = divmod(index, 3)
            button = tk.Button(
                board_frame,
                text="",
                font=self.cell_font,
                width=4,
                height=2,
                bg=PANEL,
                fg=TEXT,
                activebackground="#2e3446",
                activeforeground=TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda i=index: self.on_click(i),
            )
            button.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            self.buttons.append(button)

        actions = tk.Frame(self.root, bg=BG)
        actions.pack(pady=(4, 16))
        self._action_button(actions, "New game", self.new_game).pack(side="left", padx=6)

    def _radio(self, parent, text, value):
        return tk.Radiobutton(
            parent,
            text=text,
            value=value,
            variable=self.mode_var if value in {"computer", "human"} else self.mark_var,
            font=self.small_font,
            fg=TEXT,
            bg=BG,
            selectcolor=PANEL,
            activebackground=BG,
            activeforeground=TEXT,
            highlightthickness=0,
            command=self.new_game,
        )

    def _action_button(self, parent, text, command):
        button = tk.Button(
            parent,
            text=text,
            font=self.small_font,
            bg=BTN,
            fg="white",
            activebackground=BTN_HOVER,
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            command=command,
        )
        return button

    def new_game(self):
        self.board = [""] * 9
        self.vs_computer = self.mode_var.get() == "computer"
        self.human_mark = self.mark_var.get()
        self.computer_mark = "O" if self.human_mark == "X" else "X"
        self.turn = "X"
        self.game_over = False

        for button in self.buttons:
            button.config(text="", fg=TEXT, bg=PANEL, state="normal")

        if self.vs_computer:
            self.set_status(f"You are {self.human_mark}. Computer is {self.computer_mark}.")
            if self.turn == self.computer_mark:
                self.root.after(350, self.play_computer)
            else:
                self.set_status(f"Your turn ({self.human_mark}). Click a square.")
        else:
            self.set_status("X goes first. Click a square.")

    def set_status(self, text):
        self.status.config(text=text)

    def on_click(self, index):
        if self.game_over or self.board[index]:
            return
        if self.vs_computer and self.turn != self.human_mark:
            return

        self.place(index, self.turn)
        if self.finish_if_needed():
            return
        self.turn = "O" if self.turn == "X" else "X"

        if self.vs_computer:
            self.set_status("Computer is thinking...")
            self.root.after(280, self.play_computer)
        else:
            self.set_status(f"{self.turn}'s turn. Click a square.")

    def play_computer(self):
        if self.game_over:
            return
        index = computer_move(self.board[:], self.computer_mark)
        self.place(index, self.computer_mark)
        if self.finish_if_needed():
            return
        self.turn = self.human_mark
        self.set_status(f"Your turn ({self.human_mark}). Click a square.")

    def place(self, index, mark):
        self.board[index] = mark
        color = X_COLOR if mark == "X" else O_COLOR
        self.buttons[index].config(text=mark, fg=color)

    def finish_if_needed(self):
        found, line = winner(self.board)
        if found:
            self.game_over = True
            for i in line:
                self.buttons[i].config(bg=WIN_BG)
            if self.vs_computer:
                if found == self.human_mark:
                    self.set_status("You win!")
                else:
                    self.set_status("Computer wins.")
            else:
                self.set_status(f"{found} wins!")
            return True
        if board_full(self.board):
            self.game_over = True
            self.set_status("Draw. No one wins.")
            return True
        return False


def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
