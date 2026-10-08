"""Tic-Tac-Toe GUI. Run: python Tictactoe_gui.py"""

import tkinter as tk

from Tictactoe import WIN_LINES, board_full, minimax, winner

MARK_FIRST = "*"
MARK_SECOND = "#"
EMPTY = ""

BG = "#1b1f2a"
PANEL = "#252b3a"
CELL_BG = "#323a4d"
CELL_HOVER = "#3e4860"
WIN_BG = "#2f6f4e"
TEXT = "#f4f6fb"
MUTED = "#a8b0c4"
STAR = "#7ec8e3"
HASH = "#f0b27a"


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.board = [EMPTY] * 9
        self.buttons = []
        self.vs_computer = tk.BooleanVar(value=True)
        self.human_mark = tk.StringVar(value=MARK_FIRST)
        self.turn = MARK_FIRST
        self.game_over = False
        self.busy = False
        self._pending = None

        self._build()
        self.new_game()

    def _build(self):
        pad = {"padx": 16, "pady": 8}
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", **pad)

        tk.Label(
            header,
            text="Tic-Tac-Toe",
            font=("Segoe UI", 22, "bold"),
            fg=TEXT,
            bg=BG,
        ).pack(anchor="w")

        self.status = tk.Label(
            header,
            text="",
            font=("Segoe UI", 13),
            fg=MUTED,
            bg=BG,
        )
        self.status.pack(anchor="w", pady=(4, 0))

        board_frame = tk.Frame(self.root, bg=BG)
        board_frame.pack(padx=16, pady=8)

        for index in range(9):
            row, col = divmod(index, 3)
            button = tk.Button(
                board_frame,
                text="",
                width=4,
                height=2,
                font=("Segoe UI", 28, "bold"),
                bg=CELL_BG,
                fg=TEXT,
                activebackground=CELL_HOVER,
                activeforeground=TEXT,
                relief="flat",
                bd=0,
                command=lambda i=index: self.on_click(i),
            )
            button.grid(row=row, column=col, padx=4, pady=4, ipadx=8, ipady=8)
            button.bind("<Enter>", lambda _e, b=button: self._hover(b, True))
            button.bind("<Leave>", lambda _e, b=button: self._hover(b, False))
            self.buttons.append(button)

        controls = tk.Frame(self.root, bg=PANEL)
        controls.pack(fill="x", padx=16, pady=(8, 16))

        mode_row = tk.Frame(controls, bg=PANEL)
        mode_row.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(mode_row, text="Mode", fg=MUTED, bg=PANEL, font=("Segoe UI", 10)).pack(
            side="left"
        )
        tk.Radiobutton(
            mode_row,
            text="Vs computer",
            variable=self.vs_computer,
            value=True,
            command=self.new_game,
            fg=TEXT,
            bg=PANEL,
            selectcolor=CELL_BG,
            activebackground=PANEL,
            activeforeground=TEXT,
            font=("Segoe UI", 11),
        ).pack(side="left", padx=(12, 0))
        tk.Radiobutton(
            mode_row,
            text="Two players",
            variable=self.vs_computer,
            value=False,
            command=self.new_game,
            fg=TEXT,
            bg=PANEL,
            selectcolor=CELL_BG,
            activebackground=PANEL,
            activeforeground=TEXT,
            font=("Segoe UI", 11),
        ).pack(side="left", padx=(8, 0))

        mark_row = tk.Frame(controls, bg=PANEL)
        mark_row.pack(fill="x", padx=12, pady=4)
        tk.Label(
            mark_row,
            text="Play as",
            fg=MUTED,
            bg=PANEL,
            font=("Segoe UI", 10),
        ).pack(side="left")
        tk.Radiobutton(
            mark_row,
            text="*  (first)",
            variable=self.human_mark,
            value=MARK_FIRST,
            command=self.new_game,
            fg=TEXT,
            bg=PANEL,
            selectcolor=CELL_BG,
            activebackground=PANEL,
            activeforeground=TEXT,
            font=("Segoe UI", 11),
        ).pack(side="left", padx=(12, 0))
        tk.Radiobutton(
            mark_row,
            text="#  (second)",
            variable=self.human_mark,
            value=MARK_SECOND,
            command=self.new_game,
            fg=TEXT,
            bg=PANEL,
            selectcolor=CELL_BG,
            activebackground=PANEL,
            activeforeground=TEXT,
            font=("Segoe UI", 11),
        ).pack(side="left", padx=(8, 0))

        tk.Button(
            controls,
            text="New game",
            command=self.new_game,
            bg=CELL_BG,
            fg=TEXT,
            activebackground=CELL_HOVER,
            activeforeground=TEXT,
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=12,
            pady=6,
        ).pack(padx=12, pady=(8, 12), anchor="w")

    def _hover(self, button, entering):
        if self.game_over or button["state"] == "disabled":
            return
        if button.cget("bg") == WIN_BG:
            return
        button.configure(bg=CELL_HOVER if entering else CELL_BG)

    def computer_mark(self):
        return MARK_SECOND if self.human_mark.get() == MARK_FIRST else MARK_FIRST

    def new_game(self):
        if self._pending is not None:
            self.root.after_cancel(self._pending)
            self._pending = None
        self.board = [EMPTY] * 9
        self.turn = MARK_FIRST
        self.game_over = False
        self.busy = False
        for button in self.buttons:
            button.configure(text="", fg=TEXT, bg=CELL_BG, state="normal")
        self._set_status()
        if self.vs_computer.get() and self.human_mark.get() == MARK_SECOND:
            self.busy = True
            self._pending = self.root.after(250, self._computer_turn)

    def _set_status(self, message=None):
        if message:
            self.status.configure(text=message, fg=TEXT)
            return
        if self.vs_computer.get():
            you = self.human_mark.get()
            self.status.configure(
                text=f"Your turn ({you})" if self.turn == you else "Computer thinking...",
                fg=MUTED,
            )
        else:
            self.status.configure(text=f"{self.turn}'s turn", fg=MUTED)

    def on_click(self, index):
        if self.game_over or self.busy or self.board[index]:
            return
        if self.vs_computer.get() and self.turn != self.human_mark.get():
            return
        self._place(index, self.turn)
        if self.game_over:
            return
        if self.vs_computer.get():
            self.busy = True
            self._set_status()
            self._pending = self.root.after(250, self._computer_turn)

    def _computer_turn(self):
        if self.game_over:
            self.busy = False
            return
        _, index = minimax(self.board, self.computer_mark(), True)
        if index is not None:
            self._place(index, self.computer_mark())
        self.busy = False

    def _place(self, index, mark):
        self.board[index] = mark
        color = STAR if mark == MARK_FIRST else HASH
        self.buttons[index].configure(text=mark, fg=color, bg=CELL_BG)
        found = winner(self.board)
        if found:
            self.game_over = True
            self._highlight_win(found)
            self._set_status(f"{found} wins!")
            return
        if board_full(self.board):
            self.game_over = True
            self._set_status("Draw.")
            return
        self.turn = MARK_SECOND if mark == MARK_FIRST else MARK_FIRST
        self._set_status()

    def _highlight_win(self, mark):
        for a, b, c in WIN_LINES:
            if self.board[a] == self.board[b] == self.board[c] == mark:
                for index in (a, b, c):
                    self.buttons[index].configure(bg=WIN_BG)


def main():
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
