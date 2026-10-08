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

MAX_MARKS = 3
INFINITE_DEPTH = 8


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


def apply_move(board, history, mark, index, infinite):
    board[index] = mark
    history[mark].append(index)
    removed = None
    if infinite and len(history[mark]) > MAX_MARKS:
        removed = history[mark].pop(0)
        board[removed] = ""
    return removed


def undo_move(board, history, mark, index, removed):
    if removed is not None:
        board[removed] = mark
        history[mark].insert(0, removed)
    history[mark].pop()
    board[index] = ""


def next_vanish(history, mark):
    if len(history[mark]) >= MAX_MARKS:
        return history[mark][0]
    return None


def print_vanish_hints(history):
    for mark in ("X", "O"):
        cell = next_vanish(history, mark)
        if cell is not None:
            print(f"{mark}'s oldest mark is square {cell + 1} and will vanish on their next move.")


def minimax(board, mark, maximizing, infinite=False, history=None, depth=None, path=None):
    if history is None:
        history = {"X": [], "O": []}
    if path is None:
        path = set()

    found = winner(board)
    if found == mark:
        return 1, None
    if found:
        return -1, None
    if not infinite and board_full(board):
        return 0, None

    opponent = "O" if mark == "X" else "X"
    current = mark if maximizing else opponent

    if infinite:
        if depth is None:
            depth = INFINITE_DEPTH
        state = (tuple(board), tuple(history["X"]), tuple(history["O"]), current)
        if state in path or depth == 0:
            return 0, None

    best_score = -2 if maximizing else 2
    best_move = None
    if infinite:
        path.add(state)

    for index in empty_cells(board):
        removed = apply_move(board, history, current, index, infinite)
        score, _ = minimax(
            board,
            mark,
            not maximizing,
            infinite,
            history,
            None if not infinite else depth - 1,
            path,
        )
        undo_move(board, history, current, index, removed)
        if maximizing and score > best_score:
            best_score, best_move = score, index
        elif not maximizing and score < best_score:
            best_score, best_move = score, index

    if infinite:
        path.remove(state)

    return best_score, best_move


def computer_move(board, history, mark, infinite):
    _, index = minimax(board, mark, True, infinite=infinite, history=history)
    apply_move(board, history, mark, index, infinite)
    print(f"Computer ({mark}) plays square {index + 1}.")


def human_move(board, history, mark, infinite):
    while True:
        raw = input(f"{mark}'s turn. Pick a square (1-9): ").strip()
        if not raw.isdigit() or not 1 <= int(raw) <= 9:
            print("Enter a number from 1 to 9.")
            continue
        index = int(raw) - 1
        if board[index]:
            print("That square is taken. Try again.")
            continue
        apply_move(board, history, mark, index, infinite)
        return


def play(vs_computer, infinite):
    board = [""] * 9
    history = {"X": [], "O": []}
    human_mark = "X"
    computer_mark = "O"

    if infinite:
        print("Infinite mode: each player keeps only 3 marks. A fourth placement removes your oldest mark.")

    if vs_computer:
        choice = input("Play as X (goes first) or O? [X/O]: ").strip().upper()
        if choice == "O":
            human_mark, computer_mark = "O", "X"

    turn = "X"
    while True:
        print_board(board)
        if infinite:
            print_vanish_hints(history)
        if vs_computer and turn == computer_mark:
            computer_move(board, history, computer_mark, infinite)
        else:
            human_move(board, history, turn, infinite)

        found = winner(board)
        if found:
            print_board(board)
            print(f"{found} wins!")
            return
        if not infinite and board_full(board):
            print_board(board)
            print("Draw.")
            return
        turn = "O" if turn == "X" else "X"


def main():
    print("Tic-Tac-Toe")
    while True:
        mode = input("1 — two players, 2 — vs computer: ").strip()
        if mode not in {"1", "2"}:
            print("Choose 1 or 2.")
            continue
        variant = input("1 — classic, 2 — infinite (max 3 marks each): ").strip()
        if variant not in {"1", "2"}:
            print("Choose 1 or 2.")
            continue
        play(vs_computer=mode == "2", infinite=variant == "2")
        again = input("Play again? [y/n]: ").strip().lower()
        if again != "y":
            print("Goodbye.")
            return


if __name__ == "__main__":
    main()
