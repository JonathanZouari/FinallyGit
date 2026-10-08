"""Tic-Tac-Toe. Run: python Tictactoe.py"""

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

SYMBOL_SETS = {
    "1": ("X", "O"),
    "2": ("*", "#"),
}


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
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


def minimax(board, mark, opponent, maximizing):
    found = winner(board)
    if found == mark:
        return 1, None
    if found:
        return -1, None
    if board_full(board):
        return 0, None

    current = mark if maximizing else opponent
    best_score = -2 if maximizing else 2
    best_move = None

    for index in empty_cells(board):
        board[index] = current
        score, _ = minimax(board, mark, opponent, not maximizing)
        board[index] = ""
        if maximizing and score > best_score:
            best_score, best_move = score, index
        elif not maximizing and score < best_score:
            best_score, best_move = score, index

    return best_score, best_move


def computer_move(board, mark, opponent):
    _, index = minimax(board, mark, opponent, True)
    board[index] = mark
    print(f"Computer ({mark}) plays square {index + 1}.")


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


def choose_symbols():
    while True:
        choice = input("Symbols: 1 — X/O, 2 — * and #: ").strip()
        if choice in SYMBOL_SETS:
            return SYMBOL_SETS[choice]
        print("Choose 1 or 2.")


def play(vs_computer, symbols):
    first, second = symbols
    board = [""] * 9
    human_mark = first
    computer_mark = second

    if vs_computer:
        choice = input(
            f"Play as {first} (goes first) or {second}? [{first}/{second}]: "
        ).strip().upper()
        if choice == second:
            human_mark, computer_mark = second, first

    turn = first
    while True:
        print_board(board)
        if vs_computer and turn == computer_mark:
            computer_move(board, computer_mark, human_mark)
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
        turn = second if turn == first else first


def main():
    print("Tic-Tac-Toe")
    symbols = choose_symbols()
    while True:
        mode = input("1 — two players, 2 — vs computer: ").strip()
        if mode not in {"1", "2"}:
            print("Choose 1 or 2.")
            continue
        play(vs_computer=mode == "2", symbols=symbols)
        again = input("Play again? [y/n]: ").strip().lower()
        if again != "y":
            print("Goodbye.")
            return


if __name__ == "__main__":
    main()