"""Tic-Tac-Toe GUI. Run: python TictactoeGUI.py"""

import tkinter as tk
from tkinter import messagebox

from Tictactoe import board_full, empty_cells, minimax, winner

MARK_FIRST = "*"
MARK_SECOND = "#"


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)

        self.board = [""] * 9
        self.buttons = []
        self.turn = MARK_FIRST
        self.game_over = False
        self.vs_computer = tk.BooleanVar(value=True)
        self.human_mark = tk.StringVar(value=MARK_FIRST)

        self._build_ui()
        self.new_game()

    def _build_ui(self):
        top = tk.Frame(self.root, padx=12, pady=10)
        top.pack(fill="x")

        tk.Label(top, text="Mode:").pack(side="left")
        tk.Radiobutton(
            top,
            text="vs Computer",
            variable=self.vs_computer,
            value=True,
            command=self.new_game,
        ).pack(side="left", padx=(4, 8))
        tk.Radiobutton(
            top,
            text="Two Players",
            variable=self.vs_computer,
            value=False,
            command=self.new_game,
        ).pack(side="left")

        mark_row = tk.Frame(self.root, padx=12)
        mark_row.pack(fill="x")
        tk.Label(mark_row, text="Your mark (vs computer):").pack(side="left")
        tk.Radiobutton(
            mark_row,
            text=f"{MARK_FIRST} (first)",
            variable=self.human_mark,
            value=MARK_FIRST,
            command=self.new_game,
        ).pack(side="left", padx=(4, 8))
        tk.Radiobutton(
            mark_row,
            text=f"{MARK_SECOND} (second)",
            variable=self.human_mark,
            value=MARK_SECOND,
            command=self.new_game,
        ).pack(side="left")

        self.status = tk.Label(self.root, text="", font=("Helvetica", 14), pady=8)
        self.status.pack()

        grid = tk.Frame(self.root, padx=12, pady=4)
        grid.pack()
        for index in range(9):
            button = tk.Button(
                grid,
                text="",
                width=4,
                height=2,
                font=("Helvetica", 28, "bold"),
                command=lambda i=index: self.on_click(i),
            )
            button.grid(row=index // 3, column=index % 3, padx=3, pady=3)
            self.buttons.append(button)

        tk.Button(self.root, text="New Game", command=self.new_game, pady=6).pack(
            pady=(4, 12)
        )

    def computer_mark(self):
        return MARK_SECOND if self.human_mark.get() == MARK_FIRST else MARK_FIRST

    def refresh_board(self):
        for index, button in enumerate(self.buttons):
            mark = self.board[index]
            button.config(text=mark, state="disabled" if mark or self.game_over else "normal")

    def set_status(self, text):
        self.status.config(text=text)

    def new_game(self):
        self.board = [""] * 9
        self.turn = MARK_FIRST
        self.game_over = False
        self.refresh_board()

        if self.vs_computer.get():
            if self.human_mark.get() == MARK_FIRST:
                self.set_status(f"Your turn ({MARK_FIRST})")
            else:
                self.set_status("Computer thinking...")
                self.root.after(200, self.computer_turn)
        else:
            self.set_status(f"{MARK_FIRST}'s turn")

    def on_click(self, index):
        if self.game_over or self.board[index]:
            return
        if self.vs_computer.get() and self.turn != self.human_mark.get():
            return

        self.place(index, self.turn)
        if self.game_over:
            return

        if self.vs_computer.get():
            self.set_status("Computer thinking...")
            self.root.after(200, self.computer_turn)

    def computer_turn(self):
        if self.game_over or not self.vs_computer.get():
            return
        mark = self.computer_mark()
        if self.turn != mark:
            return
        _, index = minimax(self.board, mark, True)
        if index is None and empty_cells(self.board):
            index = empty_cells(self.board)[0]
        if index is not None:
            self.place(index, mark)

    def place(self, index, mark):
        self.board[index] = mark
        self.refresh_board()

        found = winner(self.board)
        if found:
            self.game_over = True
            self.refresh_board()
            self.set_status(f"{found} wins!")
            messagebox.showinfo("Game Over", f"{found} wins!")
            return

        if board_full(self.board):
            self.game_over = True
            self.refresh_board()
            self.set_status("Draw!")
            messagebox.showinfo("Game Over", "Draw!")
            return

        self.turn = MARK_SECOND if mark == MARK_FIRST else MARK_FIRST
        if self.vs_computer.get():
            if self.turn == self.human_mark.get():
                self.set_status(f"Your turn ({self.turn})")
            else:
                self.set_status("Computer thinking...")
        else:
            self.set_status(f"{self.turn}'s turn")
        self.refresh_board()


def main():
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
