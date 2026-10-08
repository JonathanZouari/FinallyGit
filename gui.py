"""Graphical Tic-Tac-Toe. Run: python gui.py"""

import tkinter as tk

from Tictactoe import FIRST, SECOND, WIN_LINES, board_full, minimax, other, winner

BG = "#161a22"
PANEL = "#1e2430"
CELL = "#2c3444"
CELL_HOVER = "#3a4458"
HINT_BG = "#3f4f78"
WIN_BG = "#1f6b45"
PLACES = (
    "top left",
    "top center",
    "top right",
    "middle left",
    "center",
    "middle right",
    "bottom left",
    "bottom center",
    "bottom right",
)
MARK_COLOR = {FIRST: "#ff5c5c", SECOND: "#3fd6e4"}
TEXT = "#e8edf5"
MUTED = "#9aa3b5"
ACCENT = "#4c8dff"


def next_step(board, mark):
    """Return the best square index and a short recommendation for mark."""
    found = winner(board)
    if found:
        return None, f"{found} already won. Start a new game."
    if board_full(board):
        return None, "The board is full. It's a draw."

    score, index = minimax(board, mark, True)
    trial = board[:]
    trial[index] = mark
    if winner(trial) == mark:
        reason = "That wins the game."
    elif _opponent_can_win(board, other(mark)):
        reason = "That blocks the opponent."
    elif score > 0:
        reason = "That keeps a forced win."
    elif score < 0:
        reason = "The opponent can still force a win, and this is the strongest defense."
    else:
        reason = "That keeps the game even."
    return index, f"Play {PLACES[index]} (square {index + 1}) for {mark}. {reason}"


def _opponent_can_win(board, mark):
    for index, cell in enumerate(board):
        if cell:
            continue
        probe = board[:]
        probe[index] = mark
        if winner(probe) == mark:
            return True
    return False


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
        self.hint_index = None
        self.hint_text = ""
        self._chat_state = None
        self._build()
        self.new_game()

    def _build(self):
        root = self.root
        root.title("Tic-Tac-Toe")
        root.configure(bg=BG)
        root.resizable(False, False)

        outer = tk.Frame(root, bg=BG, padx=28, pady=24)
        outer.pack()

        game = tk.Frame(outer, bg=BG)
        game.grid(row=0, column=0, sticky="n")

        tk.Label(
            game,
            text="Tic-Tac-Toe",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 22, "bold"),
        ).grid(row=0, column=0, pady=(0, 14))

        modes = tk.Frame(game, bg=BG)
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

        self.marks = tk.Frame(game, bg=BG)
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
            game,
            text="",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 14, "bold"),
        )
        self.status.grid(row=3, column=0, pady=(8, 14))

        board = tk.Frame(game, bg=BG)
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
            game,
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

        self._build_chat(outer)

    def _build_chat(self, outer):
        chat = tk.Frame(outer, bg=BG)
        chat.grid(row=0, column=1, sticky="ns", padx=(22, 0))
        tk.Label(
            chat,
            text="Coach",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", pady=(0, 8))
        self.transcript = tk.Text(
            chat,
            width=34,
            height=18,
            wrap="word",
            bg=PANEL,
            fg=TEXT,
            relief="flat",
            font=("Segoe UI", 10),
            padx=12,
            pady=10,
            state="disabled",
            cursor="arrow",
        )
        self.transcript.tag_config("name", foreground=MUTED, font=("Segoe UI", 9, "bold"))
        self.transcript.tag_config("coach", foreground="#b7cffc", spacing3=8)
        self.transcript.tag_config("you", foreground=TEXT, spacing3=8)
        self.transcript.pack(fill="both", expand=True)

        compose = tk.Frame(chat, bg=BG)
        compose.pack(fill="x", pady=(10, 0))
        self.entry = tk.Entry(
            compose,
            bg=CELL,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Segoe UI", 11),
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.entry.bind("<Return>", lambda _event: self._send())
        tk.Button(
            compose,
            text="Send",
            font=("Segoe UI", 10),
            bg=ACCENT,
            fg="white",
            activebackground="#3b74d6",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self._send,
        ).pack(side="left", padx=(8, 0))
        tk.Button(
            chat,
            text="Next step",
            font=("Segoe UI", 11),
            bg=PANEL,
            fg=TEXT,
            activebackground=CELL,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self._ask_next,
        ).pack(anchor="w", pady=(8, 0))

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
        self.hint_index = None
        self.hint_text = ""
        self._chat_state = None
        self._clear_chat()
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
        self._update_hint()
        won = self._winning_indexes()
        locked = self.game_over or self.waiting_for_computer
        for index, button in enumerate(self.buttons):
            mark = self.board[index]
            is_win = index in won
            bg = self._cell_bg(index)
            button.config(
                text=mark,
                fg=MARK_COLOR.get(mark, TEXT),
                bg=bg,
                activebackground=bg if is_win or mark or locked else CELL_HOVER,
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
        self._announce_hint()

    def _cell_bg(self, index):
        if index in self._winning_indexes():
            return WIN_BG
        if index == self.hint_index and not self.board[index]:
            return HINT_BG
        return CELL

    def _update_hint(self):
        if self.game_over or self.waiting_for_computer:
            self.hint_index = None
            return
        if self.mode == "cpu" and self.turn != self.human_mark:
            self.hint_index = None
            return
        self.hint_index, self.hint_text = next_step(self.board, self.turn)

    def _current_advice(self):
        if self.game_over:
            won = self._winning_indexes()
            if won:
                mark = self.board[won[0]]
                return f"{mark} won. Start a new game and I'll recommend the opening."
            return "It's a draw. Start a new game and I'll recommend the opening."
        if self.waiting_for_computer or (self.mode == "cpu" and self.turn != self.human_mark):
            return "The computer is moving. Ask again on your turn."
        return self.hint_text

    def _announce_hint(self):
        state = (
            tuple(self.board),
            self.turn,
            self.game_over,
            self.waiting_for_computer,
            self.mode,
            self.human_mark,
        )
        if state == self._chat_state:
            return
        self._chat_state = state
        self._append("coach", self._current_advice())

    def _ask_next(self):
        self._append("you", "What's the next step?")
        self._append("coach", self._current_advice())

    def _send(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self._append("you", text)
        self._append("coach", self._reply(text))

    def _reply(self, text):
        lowered = text.lower()
        if any(word in lowered for word in ("next", "hint", "move", "step", "recommend", "why", "צעד", "הבא", "המלצ", "למה")):
            return self._current_advice()
        return "Ask for the next step, and I'll recommend the best square."

    def _clear_chat(self):
        self.transcript.config(state="normal")
        self.transcript.delete("1.0", "end")
        self.transcript.config(state="disabled")

    def _append(self, who, message):
        label = "Coach" if who == "coach" else "You"
        self.transcript.config(state="normal")
        self.transcript.insert("end", f"{label}\n", "name")
        self.transcript.insert("end", f"{message}\n", who)
        self.transcript.config(state="disabled")
        self.transcript.see("end")

    def _on_enter(self, index):
        if self.board[index] or self.game_over or self.waiting_for_computer:
            return
        self.buttons[index].config(bg=CELL_HOVER)

    def _on_leave(self, index):
        if self.board[index] or index in self._winning_indexes():
            return
        self.buttons[index].config(bg=self._cell_bg(index))


def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
