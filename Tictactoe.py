"""Tic-Tac-Toe on a 3x3, 4x4, or 5x5 board. Run: python Tictactoe.py"""

MAX_DEPTH = {3: 9, 4: 4, 5: 3}


def win_length_for(size):
    return 3 if size == 3 else 4


def make_win_lines(size, win_len):
    lines = []
    for row in range(size):
        for col in range(size - win_len + 1):
            start = row * size + col
            lines.append(tuple(start + i for i in range(win_len)))
    for col in range(size):
        for row in range(size - win_len + 1):
            lines.append(tuple((row + i) * size + col for i in range(win_len)))
    for row in range(size - win_len + 1):
        for col in range(size - win_len + 1):
            lines.append(tuple((row + i) * size + (col + i) for i in range(win_len)))
    for row in range(size - win_len + 1):
        for col in range(win_len - 1, size):
            lines.append(tuple((row + i) * size + (col - i) for i in range(win_len)))
    return tuple(lines)


def winner(board, lines):
    for line in lines:
        first = board[line[0]]
        if first and all(board[i] == first for i in line):
            return first
    return None


def board_full(board):
    return all(board)


def print_board(board, size):
    width = len(str(size * size))

    def show(index):
        value = board[index] if board[index] else str(index + 1)
        return value.rjust(width)

    rows = [
        " | ".join(show(row * size + col) for col in range(size))
        for row in range(size)
    ]
    divider = "\n" + "".join("+" if ch == "|" else "-" for ch in rows[0]) + "\n"
    print("\n" + divider.join(rows) + "\n")


def empty_cells(board):
    return [index for index, cell in enumerate(board) if not cell]


def evaluate(board, mark, lines):
    found = winner(board, lines)
    if found == mark:
        return 1000
    if found:
        return -1000

    opponent = "O" if mark == "X" else "X"
    score = 0
    for line in lines:
        values = [board[i] for i in line]
        if opponent not in values:
            count = values.count(mark)
            score += count * count
        elif mark not in values:
            count = values.count(opponent)
            score -= count * count
    return score


def minimax(board, mark, maximizing, depth, max_depth, lines, alpha, beta):
    found = winner(board, lines)
    if found == mark:
        return 1000 - depth, None
    if found:
        return depth - 1000, None
    if board_full(board) or depth == max_depth:
        return evaluate(board, mark, lines), None

    opponent = "O" if mark == "X" else "X"
    current = mark if maximizing else opponent
    best_score = -10_000 if maximizing else 10_000
    best_move = None

    for index in empty_cells(board):
        board[index] = current
        score, _ = minimax(
            board, mark, not maximizing, depth + 1, max_depth, lines, alpha, beta
        )
        board[index] = ""
        if maximizing:
            if score > best_score:
                best_score, best_move = score, index
            alpha = max(alpha, score)
        else:
            if score < best_score:
                best_score, best_move = score, index
            beta = min(beta, score)
        if beta <= alpha:
            break

    return best_score, best_move


def computer_move(board, mark, size, lines):
    _, index = minimax(
        board,
        mark,
        True,
        0,
        MAX_DEPTH[size],
        lines,
        -10_000,
        10_000,
    )
    if index is None:
        index = empty_cells(board)[0]
    board[index] = mark
    print(f"Computer ({mark}) plays square {index + 1}.")


def human_move(board, mark, size):
    last = size * size
    while True:
        raw = input(f"{mark}'s turn. Pick a square (1-{last}): ").strip()
        if not raw.isdigit() or not 1 <= int(raw) <= last:
            print(f"Enter a number from 1 to {last}.")
            continue
        index = int(raw) - 1
        if board[index]:
            print("That square is taken. Try again.")
            continue
        board[index] = mark
        return


def play(vs_computer, size):
    win_len = win_length_for(size)
    lines = make_win_lines(size, win_len)
    board = [""] * (size * size)
    human_mark = "X"
    computer_mark = "O"

    print(f"\n{size}x{size} board — get {win_len} in a row to win.")

    if vs_computer:
        choice = input("Play as X (goes first) or O? [X/O]: ").strip().upper()
        if choice == "O":
            human_mark, computer_mark = "O", "X"

    turn = "X"
    while True:
        print_board(board, size)
        if vs_computer and turn == computer_mark:
            computer_move(board, computer_mark, size, lines)
        else:
            human_move(board, turn, size)

        found = winner(board, lines)
        if found:
            print_board(board, size)
            print(f"{found} wins!")
            return
        if board_full(board):
            print_board(board, size)
            print("Draw.")
            return
        turn = "O" if turn == "X" else "X"


def choose_size():
    while True:
        raw = input("Board size — 3, 4, or 5: ").strip()
        if raw in {"3", "4", "5"}:
            return int(raw)
        print("Choose 3, 4, or 5.")


def main():
    print("Tic-Tac-Toe")
    while True:
        size = choose_size()
        mode = input("1 — two players, 2 — vs computer: ").strip()
        if mode not in {"1", "2"}:
            print("Choose 1 or 2.")
            continue
        play(vs_computer=mode == "2", size=size)
        again = input("Play again? [y/n]: ").strip().lower()
        if again != "y":
            print("Goodbye.")
            return


if __name__ == "__main__":
    main()
