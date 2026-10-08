"""Tic-Tac-Toe. Run: python Tictactoe.py (GUI) or python Tictactoe.py --cli"""

import argparse
import tkinter as tk

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

BG = "#1a2332"
PANEL = "#243044"
CELL = "#2f4058"
CELL_HOVER = "#3d5474"
WIN_CELL = "#2d6a4f"
X_COLOR = "#7dd3fc"
O_COLOR = "#f9a8d4"
TEXT = "#e8eef7"
MUTED = "#9fb0c7"


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


def print_board(board):
    def show(index):
        return board[index] if board[index] else str(index + 1)

    rows = [" | ".join(show(row * 3 + col) for col in range(3)) for row in range(3)]
    print("\n" + "\n--+---+--\n".join(rows) + "\n")


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


def best_move(board, mark):
    _, index = minimax(board, mark, True)
    return index


def computer_move(board, mark):
    index = best_move(board, mark)
    board[index] = mark
    print(f"Computer ({mark}) plays square {index + 1}.")
    return index


def human_move(board, mark):
    while True:
        raw = input(f"{mark}'s turn. Pick a square (1-9): ").strip()
        if not raw.isdigit() or not 1 <= int(raw) <= 9:
            print("Enter a number from 1 to 9.")
            continue
        index = int(raw) - 1
        if board[index]:
            print("That square is taken. Try again.")
            continue
        board[index] = mark
        return


def play(vs_computer):
    board = [""] * 9
    human_mark = "X"
    computer_mark = "O"

    if vs_computer:
        choice = input("Play as X (goes first) or O? [X/O]: ").strip().upper()
        if choice == "O":
            human_mark, computer_mark = "O", "X"

    turn = "X"
    while True:
        print_board(board)
        if vs_computer and turn == computer_mark:
            computer_move(board, computer_mark)
        else:
            human_move(board, turn)

        found = winner(board)
        if found:
            print_board(board)
            print(f"{found} wins!")
            return
        if board_full(board):
            print_board(board)
            print("Draw.")
            return
        turn = "O" if turn == "X" else "X"


def cli_main():
    print("Tic-Tac-Toe")
    while True:
        mode = input("1 — two players, 2 — vs computer: ").strip()
        if mode not in {"1", "2"}:
            print("Choose 1 or 2.")
            continue
        play(vs_computer=mode == "2")
        again = input("Play again? [y/n]: ").strip().lower()
        if again != "y":
            print("Goodbye.")
            return


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("איקס עיגול")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.board = [""] * 9
        self.vs_computer = tk.BooleanVar(value=True)
        self.human_mark = tk.StringVar(value="X")
        self.turn = "X"
        self.over = False
        self.busy = False
        self.cells = []

        self._build()
        self.new_game()

    def _build(self):
        pad = {"padx": 16, "pady": 8}
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", **pad)

        tk.Label(
            header,
            text="איקס עיגול",
            font=("Segoe UI", 22, "bold"),
            fg=TEXT,
            bg=BG,
        ).pack()

        self.status = tk.Label(
            header,
            text="",
            font=("Segoe UI", 13),
            fg=MUTED,
            bg=BG,
        )
        self.status.pack(pady=(4, 0))

        controls = tk.Frame(self.root, bg=PANEL)
        controls.pack(fill="x", padx=16, pady=(0, 8))

        modes = tk.Frame(controls, bg=PANEL)
        modes.pack(pady=10)
        tk.Radiobutton(
            modes,
            text="מול מחשב",
            variable=self.vs_computer,
            value=True,
            command=self.new_game,
            font=("Segoe UI", 11),
            fg=TEXT,
            bg=PANEL,
            selectcolor=CELL,
            activebackground=PANEL,
            activeforeground=TEXT,
        ).pack(side="right", padx=8)
        tk.Radiobutton(
            modes,
            text="שני שחקנים",
            variable=self.vs_computer,
            value=False,
            command=self.new_game,
            font=("Segoe UI", 11),
            fg=TEXT,
            bg=PANEL,
            selectcolor=CELL,
            activebackground=PANEL,
            activeforeground=TEXT,
        ).pack(side="right", padx=8)

        self.marks = tk.Frame(controls, bg=PANEL)
        self.marks.pack(pady=(0, 10))
        tk.Label(self.marks, text="אתה משחק כ־", font=("Segoe UI", 11), fg=MUTED, bg=PANEL).pack(
            side="right"
        )
        for mark in ("X", "O"):
            tk.Radiobutton(
                self.marks,
                text=mark,
                variable=self.human_mark,
                value=mark,
                command=self.new_game,
                font=("Segoe UI", 11, "bold"),
                fg=X_COLOR if mark == "X" else O_COLOR,
                bg=PANEL,
                selectcolor=CELL,
                activebackground=PANEL,
                activeforeground=TEXT,
            ).pack(side="right", padx=6)

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
                bg=CELL,
                fg=TEXT,
                activebackground=CELL_HOVER,
                relief="flat",
                bd=0,
                command=lambda i=index: self.on_click(i),
            )
            button.grid(row=row, column=col, padx=4, pady=4, ipadx=8, ipady=8)
            button.bind("<Enter>", lambda _e, b=button: self._hover(b, True))
            button.bind("<Leave>", lambda _e, b=button: self._hover(b, False))
            self.cells.append(button)

        tk.Button(
            self.root,
            text="משחק חדש",
            font=("Segoe UI", 12, "bold"),
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            relief="flat",
            command=self.new_game,
            padx=16,
            pady=8,
        ).pack(pady=(4, 16))

    def _hover(self, button, entering):
        if self.over or button["state"] == "disabled":
            return
        if button["bg"] == WIN_CELL:
            return
        button.configure(bg=CELL_HOVER if entering else CELL)

    def new_game(self):
        self.board = [""] * 9
        self.turn = "X"
        self.over = False
        self.busy = False
        if self.vs_computer.get():
            self.marks.pack(pady=(0, 10))
        else:
            self.marks.pack_forget()
        for button in self.cells:
            button.configure(text="", fg=TEXT, bg=CELL, state="normal")
        self._refresh_status()
        if self.vs_computer.get() and self.human_mark.get() == "O":
            self.root.after(250, self._computer_turn)

    def _refresh_status(self):
        if self.over:
            return
        if self.vs_computer.get():
            human = self.human_mark.get()
            if self.turn == human:
                self.status.configure(text=f"התור שלך ({human})")
            else:
                self.status.configure(text="המחשב חושב…")
        else:
            self.status.configure(text=f"תור של {self.turn}")

    def on_click(self, index):
        if self.over or self.busy or self.board[index]:
            return
        if self.vs_computer.get() and self.turn != self.human_mark.get():
            return
        self._place(index, self.turn)
        if not self.over and self.vs_computer.get():
            self.root.after(280, self._computer_turn)

    def _computer_turn(self):
        if self.over:
            return
        computer_mark = "O" if self.human_mark.get() == "X" else "X"
        if self.turn != computer_mark:
            return
        self.busy = True
        self._refresh_status()
        self._place(best_move(self.board, computer_mark), computer_mark)
        self.busy = False

    def _place(self, index, mark):
        self.board[index] = mark
        color = X_COLOR if mark == "X" else O_COLOR
        self.cells[index].configure(text=mark, fg=color, bg=CELL)
        found = winner(self.board)
        if found:
            self.over = True
            line = winning_line(self.board)
            for i in line:
                self.cells[i].configure(bg=WIN_CELL)
            if self.vs_computer.get() and found == self.human_mark.get():
                extra = " — אתה"
            elif self.vs_computer.get():
                extra = " — המחשב"
            else:
                extra = ""
            self.status.configure(text=f"{found} ניצח{extra}!")
            return
        if board_full(self.board):
            self.over = True
            self.status.configure(text="תיקו")
            return
        self.turn = "O" if self.turn == "X" else "X"
        self._refresh_status()


def gui_main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description="Tic-Tac-Toe")
    parser.add_argument("--cli", action="store_true", help="Play in the terminal")
    args, _unknown = parser.parse_known_args()
    if args.cli:
        cli_main()
        return
    gui_main()


if __name__ == "__main__":
    main()
