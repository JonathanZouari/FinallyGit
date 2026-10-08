"""Tic-Tac-Toe. Run: python Tictactoe.py"""

import sys

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
FIRST = "*"
SECOND = "#"
PLAYER_COLOR = {
    FIRST: "\033[91m",
    SECOND: "\033[96m",
}

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
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def board_full(board):
    return all(board)


def enable_color():
    if sys.platform != "win32":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except OSError:
        pass


def color_mark(mark):
    return f"{BOLD}{PLAYER_COLOR[mark]}{mark}{RESET}"


def other(mark):
    return SECOND if mark == FIRST else FIRST


def print_board(board):
    def show(index):
        cell = board[index]
        if cell:
            return color_mark(cell)
        return f"{DIM}{index + 1}{RESET}"

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


def computer_move(board, mark):
    _, index = minimax(board, mark, True)
    board[index] = mark
    print(f"Computer ({color_mark(mark)}) plays square {index + 1}.")


def human_move(board, mark):
    while True:
        raw = input(f"{color_mark(mark)}'s turn. Pick a square (1-9): ").strip()
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
    human_mark = FIRST
    computer_mark = SECOND

    if vs_computer:
        choice = input(
            f"Play as {color_mark(FIRST)} (goes first) or {color_mark(SECOND)}? "
            f"[{FIRST}/{SECOND}]: "
        ).strip()
        if choice == SECOND:
            human_mark, computer_mark = SECOND, FIRST

    turn = FIRST
    while True:
        print_board(board)
        if vs_computer and turn == computer_mark:
            computer_move(board, computer_mark)
        else:
            human_move(board, turn)

        found = winner(board)
        if found:
            print_board(board)
            print(f"{color_mark(found)} wins!")
            return
        if board_full(board):
            print_board(board)
            print("Draw.")
            return
        turn = other(turn)


def main():
    enable_color()
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


if __name__ == "__main__":
    main()
