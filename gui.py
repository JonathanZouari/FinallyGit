"""Graphical Tic-Tac-Toe. Run: python gui.py"""

import tkinter as tk

from Tictactoe import FIRST, SECOND, WIN_LINES, board_full, minimax, other, winner

BG = "#161a22"
PANEL = "#1e2430"
CELL = "#2c3444"
CELL_HOVER = "#3a4458"
WIN_BG = "#1f6b45"
MARK_COLOR = {FIRST: "#ff5c5c", SECOND: "#3fd6e4"}
TEXT = "#e8edf5"
MUTED = "#9aa3b5"
ACCENT = "#4c8dff"


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.mode = "cpu"
        self.human_mark = FIRST
        self.board = [""] * 9
        self.turn = FIRST
        self.game_over = False
        self.waiting_for_computer = False
        self.move_token = 0
        self.buttons = []
        self._build()
        self.new_game()

    def _build(self):
        root = self.root
        root.title("Tic-Tac-Toe")
        root.configure(bg=BG)
        root.resizable(False, False)

        outer = tk.Frame(root, bg=BG, padx=28, pady=24)
        outer.pack()

        tk.Label(
            outer,
            text="Tic-Tac-Toe",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 22, "bold"),
        ).grid(row=0, column=0, pady=(0, 14))

        modes = tk.Frame(outer, bg=BG)
        modes.grid(row=1, column=0, pady=(0, 12))
        self.mode_buttons = {}
        for key, label in (("pvp", "Two players"), ("cpu", "Vs computer")):
            button = tk.Button(
                modes,
                text=label,
                font=("Segoe UI", 11),
                relief="flat",
                bd=0,
                padx=14,
                pady=8,
                cursor="hand2",
                command=lambda mode=key: self.set_mode(mode),
            )
            button.pack(side="left", padx=4)
            self.mode_buttons[key] = button

        self.marks = tk.Frame(outer, bg=BG)
        self.marks.grid(row=2, column=0, pady=(0, 4))
        tk.Label(
            self.marks,
            text="You play",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 11),
        ).pack(side="left", padx=(0, 8))
        self.mark_buttons = {}
        for mark in (FIRST, SECOND):
            button = tk.Button(
                self.marks,
                text=mark,
                font=("Segoe UI", 16, "bold"),
                fg=MARK_COLOR[mark],
                width=3,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda chosen=mark: self.set_human_mark(chosen),
            )
            button.pack(side="left", padx=4)
            self.mark_buttons[mark] = button

        self.status = tk.Label(
            outer,
            text="",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 14, "bold"),
        )
        self.status.grid(row=3, column=0, pady=(8, 14))

        board = tk.Frame(outer, bg=BG)
        board.grid(row=4, column=0)
        for index in range(9):
            cell = tk.Frame(board, width=108, height=108, bg=CELL)
            cell.grid(row=index // 3, column=index % 3, padx=5, pady=5)
            cell.pack_propagate(False)
            button = tk.Button(
                cell,
                text="",
                font=("Segoe UI", 32, "bold"),
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda square=index: self.on_click(square),
            )
            button.pack(fill="both", expand=True)
            button.bind("<Enter>", lambda _event, square=index: self._on_enter(square))
            button.bind("<Leave>", lambda _event, square=index: self._on_leave(square))
            self.buttons.append(button)

        tk.Button(
            outer,
            text="New game",
            font=("Segoe UI", 11),
            bg=ACCENT,
            fg="white",
            activebackground="#3b74d6",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.new_game,
        ).grid(row=5, column=0, pady=(16, 0))

    def set_mode(self, mode):
        if mode == self.mode:
            return
        self.mode = mode
        self.new_game()

    def set_human_mark(self, mark):
        if self.mode != "cpu" or mark == self.human_mark:
            return
        self.human_mark = mark
        self.new_game()

    def new_game(self):
        self.move_token += 1
        self.board = [""] * 9
        self.turn = FIRST
        self.game_over = False
        self.waiting_for_computer = False
        self._style_controls()
        self._finish_if_computer_opens()

    def _style_controls(self):
        for key, button in self.mode_buttons.items():
            selected = key == self.mode
            button.config(
                bg=ACCENT if selected else PANEL,
                fg="white" if selected else MUTED,
                activebackground=ACCENT if selected else "#343c4e",
                activeforeground="white",
            )
        if self.mode == "cpu":
            self.marks.grid()
        else:
            self.marks.grid_remove()
        for mark, button in self.mark_buttons.items():
            selected = mark == self.human_mark
            button.config(bg=CELL if selected else BG, activebackground=CELL)

    def on_click(self, index):
        if self.game_over or self.waiting_for_computer or self.board[index]:
            return
        if self.mode == "cpu" and self.turn != self.human_mark:
            return
        self.board[index] = self.turn
        self._finish_turn()

    def _finish_if_computer_opens(self):
        if self.mode == "cpu" and self.turn != self.human_mark:
            self._schedule_computer()
        else:
            self._paint()

    def _finish_turn(self):
        if winner(self.board) or board_full(self.board):
            self.game_over = True
            self.waiting_for_computer = False
            self._paint()
            return
        self.turn = other(self.turn)
        if self.mode == "cpu" and self.turn != self.human_mark:
            self._schedule_computer()
        else:
            self._paint()

    def _schedule_computer(self):
        self.waiting_for_computer = True
        self._paint()
        token = self.move_token
        self.root.after(180, lambda: self._computer_turn(token))

    def _computer_turn(self, token):
        if token != self.move_token or self.game_over:
            return
        self.waiting_for_computer = False
        _, index = minimax(self.board, self.turn, True)
        self.board[index] = self.turn
        self._finish_turn()

    def _winning_indexes(self):
        for line in WIN_LINES:
            a, b, c = line
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return line
        return ()

    def _paint(self):
        won = self._winning_indexes()
        locked = self.game_over or self.waiting_for_computer
        for index, button in enumerate(self.buttons):
            mark = self.board[index]
            is_win = index in won
            button.config(
                text=mark,
                fg=MARK_COLOR.get(mark, TEXT),
                bg=WIN_BG if is_win else CELL,
                activebackground=WIN_BG if is_win or mark or locked else CELL_HOVER,
                state="normal",
                cursor="arrow" if mark or locked else "hand2",
            )
        if won:
            mark = self.board[won[0]]
            self.status.config(text=f"{mark} wins", fg=MARK_COLOR[mark])
        elif self.game_over:
            self.status.config(text="Draw", fg=TEXT)
        elif self.waiting_for_computer:
            self.status.config(
                text=f"Computer plays {self.turn}",
                fg=MARK_COLOR[self.turn],
            )
        else:
            self.status.config(text=f"{self.turn} to move", fg=MARK_COLOR[self.turn])

    def _on_enter(self, index):
        if self.board[index] or self.game_over or self.waiting_for_computer:
            return
        self.buttons[index].config(bg=CELL_HOVER)

    def _on_leave(self, index):
        if self.board[index] or index in self._winning_indexes():
            return
        self.buttons[index].config(bg=CELL)


def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
