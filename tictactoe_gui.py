"""Tic-Tac-Toe GUI. Run: python tictactoe_gui.py"""

import tkinter as tk
from tkinter import ttk

from Tictactoe import WIN_LINES, board_full, minimax, winner

BG = "#1e1e2e"
PANEL = "#313244"
TEXT = "#cdd6f4"
MUTED = "#a6adc8"
ACCENT = "#89b4fa"
X_COLOR = "#f38ba8"
O_COLOR = "#89b4fa"
WIN_BG = "#45475a"
EMPTY_BG = "#45475a"


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.board = [""] * 9
        self.turn = "X"
        self.vs_computer = True
        self.human_mark = "X"
        self.computer_mark = "O"
        self.game_over = False
        self.busy = False
        self.cells = []

        self._build()
        self.new_game()

    def _build(self):
        pad = {"padx": 16, "pady": 8}
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True, **pad)

        tk.Label(
            frame,
            text="Tic-Tac-Toe",
            font=("Segoe UI", 22, "bold"),
            fg=TEXT,
            bg=BG,
        ).pack(pady=(8, 4))

        self.status = tk.Label(
            frame,
            text="",
            font=("Segoe UI", 13),
            fg=MUTED,
            bg=BG,
        )
        self.status.pack(pady=(0, 8))

        controls = tk.Frame(frame, bg=BG)
        controls.pack(pady=4)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TRadiobutton", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))

        self.mode_var = tk.StringVar(value="computer")
        ttk.Radiobutton(
            controls,
            text="Vs computer",
            variable=self.mode_var,
            value="computer",
            command=self._on_settings_change,
        ).pack(side="left", padx=6)
        ttk.Radiobutton(
            controls,
            text="Two players",
            variable=self.mode_var,
            value="human",
            command=self._on_settings_change,
        ).pack(side="left", padx=6)

        self.mark_frame = tk.Frame(frame, bg=BG)
        self.mark_frame.pack(pady=4)
        self.mark_var = tk.StringVar(value="X")
        ttk.Radiobutton(
            self.mark_frame,
            text="Play as X (first)",
            variable=self.mark_var,
            value="X",
            command=self._on_settings_change,
        ).pack(side="left", padx=6)
        ttk.Radiobutton(
            self.mark_frame,
            text="Play as O",
            variable=self.mark_var,
            value="O",
            command=self._on_settings_change,
        ).pack(side="left", padx=6)

        board_frame = tk.Frame(frame, bg=PANEL, padx=8, pady=8)
        board_frame.pack(pady=12)

        for index in range(9):
            row, col = divmod(index, 3)
            button = tk.Button(
                board_frame,
                text="",
                font=("Segoe UI", 28, "bold"),
                width=3,
                height=1,
                bg=EMPTY_BG,
                fg=TEXT,
                activebackground="#585b70",
                relief="flat",
                cursor="hand2",
                command=lambda i=index: self.on_click(i),
            )
            button.grid(row=row, column=col, padx=4, pady=4, ipadx=8, ipady=12)
            self.cells.append(button)

        ttk.Button(frame, text="New game", command=self.new_game).pack(pady=(4, 12))

    def _on_settings_change(self):
        self.new_game()

    def new_game(self):
        self.board = [""] * 9
        self.turn = "X"
        self.game_over = False
        self.busy = False
        self.vs_computer = self.mode_var.get() == "computer"
        self.human_mark = self.mark_var.get()
        self.computer_mark = "O" if self.human_mark == "X" else "X"

        if self.vs_computer:
            self.mark_frame.pack(pady=4)
        else:
            self.mark_frame.pack_forget()

        for button in self.cells:
            button.config(text="", fg=TEXT, bg=EMPTY_BG, state="normal")

        self._update_status()
        if self.vs_computer and self.turn == self.computer_mark:
            self.busy = True
            self.root.after(350, self._computer_turn)

    def on_click(self, index):
        if self.game_over or self.busy or self.board[index]:
            return
        if self.vs_computer and self.turn != self.human_mark:
            return

        self._place(index, self.turn)
        if self.game_over:
            return

        if self.vs_computer:
            self.busy = True
            self.root.after(280, self._computer_turn)

    def _computer_turn(self):
        if self.game_over:
            self.busy = False
            return
        _, index = minimax(self.board, self.computer_mark, True)
        if index is not None:
            self._place(index, self.computer_mark)
        self.busy = False

    def _place(self, index, mark):
        self.board[index] = mark
        color = X_COLOR if mark == "X" else O_COLOR
        self.cells[index].config(text=mark, fg=color)

        found = winner(self.board)
        if found:
            self.game_over = True
            self._highlight_win(found)
            self.status.config(text=f"{found} wins!", fg=X_COLOR if found == "X" else O_COLOR)
            return
        if board_full(self.board):
            self.game_over = True
            self.status.config(text="Draw.", fg=MUTED)
            return

        self.turn = "O" if self.turn == "X" else "X"
        self._update_status()

    def _highlight_win(self, mark):
        for a, b, c in WIN_LINES:
            if self.board[a] == self.board[b] == self.board[c] == mark:
                for i in (a, b, c):
                    self.cells[i].config(bg=WIN_BG)
                break

    def _update_status(self):
        if self.vs_computer:
            if self.turn == self.human_mark:
                self.status.config(text=f"Your turn ({self.human_mark})", fg=ACCENT)
            else:
                self.status.config(text="Computer is thinking…", fg=MUTED)
        else:
            self.status.config(text=f"{self.turn}'s turn", fg=ACCENT)


def main():
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
