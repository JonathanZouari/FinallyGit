"""Tic-Tac-Toe desktop GUI. Run: python Tictactoe_gui.py"""

import threading
import tkinter as tk
from tkinter import ttk

from Tictactoe import (
    board_full,
    choose_computer_index,
    make_win_lines,
    win_length_for,
    winner,
    winning_line,
)

BG = "#15181f"
PANEL = "#1f2430"
CELL = "#2a3140"
CELL_HOVER = "#3a4356"
CELL_WIN = "#14532d"
TEXT = "#e8eef7"
MUTED = "#9aa6b8"
X_COLOR = "#22d3ee"
O_COLOR = "#facc15"
ACCENT = "#7c9cff"


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("איקס עיגול")
        self.root.configure(bg=BG)
        self.root.minsize(460, 560)

        self.size = tk.IntVar(value=3)
        self.vs_computer = tk.BooleanVar(value=True)
        self.human_mark = tk.StringVar(value="X")
        self.board = []
        self.lines = ()
        self.buttons = []
        self.turn = "X"
        self.busy = False
        self.over = False

        self._style()
        self._build()
        self.new_game()

    def _style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure(
            "TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 11),
        )
        style.configure(
            "Title.TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "Status.TLabel",
            background=BG,
            foreground=ACCENT,
            font=("Segoe UI", 13, "bold"),
        )
        style.configure(
            "TRadiobutton",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 10),
        )
        style.map("TRadiobutton", background=[("active", BG)])
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=8,
        )

    def _build(self):
        pad = {"padx": 16, "pady": 6}
        ttk.Label(self.root, text="איקס עיגול", style="Title.TLabel").pack(
            pady=(16, 4)
        )

        controls = ttk.Frame(self.root)
        controls.pack(fill="x", **pad)

        ttk.Label(controls, text="לוח:").grid(row=0, column=0, sticky="w")
        for i, size in enumerate((3, 4, 5), start=1):
            ttk.Radiobutton(
                controls,
                text=f"{size}×{size}",
                value=size,
                variable=self.size,
                command=self.new_game,
            ).grid(row=0, column=i, padx=4)

        ttk.Label(controls, text="מצב:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Radiobutton(
            controls,
            text="שני שחקנים",
            value=False,
            variable=self.vs_computer,
            command=self.new_game,
        ).grid(row=1, column=1, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Radiobutton(
            controls,
            text="מול מחשב",
            value=True,
            variable=self.vs_computer,
            command=self.new_game,
        ).grid(row=1, column=3, sticky="w", pady=(8, 0))

        ttk.Label(controls, text="שחק כ:").grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Radiobutton(
            controls,
            text="X",
            value="X",
            variable=self.human_mark,
            command=self.new_game,
        ).grid(row=2, column=1, sticky="w", pady=(8, 0))
        ttk.Radiobutton(
            controls,
            text="O",
            value="O",
            variable=self.human_mark,
            command=self.new_game,
        ).grid(row=2, column=2, sticky="w", pady=(8, 0))

        ttk.Button(
            self.root, text="משחק חדש", style="Accent.TButton", command=self.new_game
        ).pack(pady=8)

        self.status = ttk.Label(self.root, text="", style="Status.TLabel")
        self.status.pack(pady=(0, 8))

        self.board_frame = tk.Frame(self.root, bg=BG, padx=16, pady=8)
        self.board_frame.pack(expand=True, fill="both")

        hint = ttk.Label(
            self.root,
            text="X בציאן, O בצהוב  ·  בלוח 4×4 ו־5×5 צריך 4 ברצף",
            foreground=MUTED,
        )
        hint.pack(pady=(0, 14))

    def new_game(self):
        size = self.size.get()
        win_len = win_length_for(size)
        self.lines = make_win_lines(size, win_len)
        self.board = [""] * (size * size)
        self.turn = "X"
        self.busy = False
        self.over = False
        self._draw_board(size)
        self._set_status(f"תור {self.turn}  ·  {win_len} ברצף לניצחון")
        if self._computer_should_play():
            self.root.after(200, self._computer_turn)

    def _draw_board(self, size):
        for child in self.board_frame.winfo_children():
            child.destroy()
        self.buttons = []
        font_size = 28 if size == 3 else 22 if size == 4 else 18
        for row in range(size):
            self.board_frame.grid_rowconfigure(row, weight=1)
            self.board_frame.grid_columnconfigure(row, weight=1)
        for index in range(size * size):
            row, col = divmod(index, size)
            button = tk.Button(
                self.board_frame,
                text="",
                font=("Segoe UI", font_size, "bold"),
                bg=CELL,
                fg=TEXT,
                activebackground=CELL_HOVER,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda i=index: self.on_click(i),
            )
            button.grid(row=row, column=col, sticky="nsew", padx=4, pady=4, ipady=12)
            self.buttons.append(button)

    def on_click(self, index):
        if self.over or self.busy or self.board[index]:
            return
        if self.vs_computer.get() and self.turn != self.human_mark.get():
            return
        self._place(index, self.turn)

    def _place(self, index, mark):
        self.board[index] = mark
        color = X_COLOR if mark == "X" else O_COLOR
        self.buttons[index].configure(text=mark, fg=color, disabledforeground=color)
        found = winner(self.board, self.lines)
        if found:
            self.over = True
            self._highlight_win()
            self._set_status(f"{found} ניצח!")
            return
        if board_full(self.board):
            self.over = True
            self._set_status("תיקו")
            return
        self.turn = "O" if self.turn == "X" else "X"
        self._set_status(f"תור {self.turn}")
        if self._computer_should_play():
            self.root.after(180, self._computer_turn)

    def _computer_should_play(self):
        if self.over or not self.vs_computer.get():
            return False
        computer_mark = "O" if self.human_mark.get() == "X" else "X"
        return self.turn == computer_mark

    def _computer_turn(self):
        if not self._computer_should_play():
            return
        self.busy = True
        self._set_status("המחשב חושב...")
        mark = self.turn
        snapshot = list(self.board)
        size = self.size.get()
        lines = self.lines

        def work():
            index = choose_computer_index(snapshot, mark, size, lines)
            self.root.after(0, lambda: self._finish_computer(index, mark))

        threading.Thread(target=work, daemon=True).start()

    def _finish_computer(self, index, mark):
        self.busy = False
        if self.over or self.board[index]:
            return
        self._place(index, mark)

    def _highlight_win(self):
        line = winning_line(self.board, self.lines)
        if not line:
            return
        for index in line:
            mark = self.board[index]
            color = X_COLOR if mark == "X" else O_COLOR
            self.buttons[index].configure(bg=CELL_WIN, fg=color, disabledforeground=color)

    def _set_status(self, text):
        self.status.configure(text=text)


def main():
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
