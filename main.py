import curses

pieces = ["o", "x"]

logging_idx = 25

def has_won(board, player, x, y):
    line = pieces[player] * 5

    directions = [
        board[y],  # Horizontal
        "".join([row[x] for row in board]),  # Vertical
        "",  # NW -> SE Diagonal
        "",
    ]

    for i, row in enumerate(board):
        try:
            directions[2] += row[y - x + i]
        except:
            pass
        try:
            directions[3] += row[y + x - i]
        except:
            pass

    return any(line in direction for direction in directions)


def draw_board(scr, board, message):
    scr.addstr(0, 0, f"+-------------------------------+")
    for i, row in enumerate(board):
        v = " ".join(list(row))
        scr.addstr(i + 1, 0, f"| {v} |")
    scr.addstr(i + 2, 0, f"+-------------------------------+")
    scr.addstr(i + 4, 0, message)
    scr.addstr(i + 6, 0, "(p)lace (r)eset (q)uit")


def board_to_screen_pos(x, y):
    return (
        y + 1,
        (x + 1) * 2,
    )


def wrapper(func, *args, **kwds):
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)
        # Some TERM's ERR out when attempting to hide cursor
        try:
            curses.curs_set(0)
        except:
            pass
        return func(stdscr, *args, **kwds)
    finally:
        if "stdscr" in locals():
            stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()


controls = {
    "reset": ["r"],
    "place": ["p"],
    "quit": ["q", "KEY_ESCAPE"],
    "left": ["KEY_LEFT", "h"],
    "right": ["KEY_RIGHT", "l"],
    "up": ["KEY_UP", "k"],
    "down": ["KEY_DOWN", "j"],
}


def main(stdscr):
    board = [" " * 15] * 15
    player = 0
    x = 7
    y = 7
    completed = False

    while True:
        message = f"{pieces[player]}'s turn to play"
        draw_board(stdscr, board, message)
        stdscr.addch(*board_to_screen_pos(x, y), board[y][x], curses.A_REVERSE)
        key = stdscr.getkey()
        stdscr.refresh()
        if not completed:
            if key in controls["place"] and board[y][x] == " ":
                row = board[y]
                board[y] = row[:x] + pieces[player] + row[x + 1 :]
                if has_won(board, player, x, y):
                    completed = True
                else:
                    player = abs(player - 1)
            elif key in controls["right"]:
                x = min(x + 1, 14)
            elif key in controls["left"]:
                x = max(x - 1, 0)
            elif key in controls["up"]:
                y = max(y - 1, 0)
            elif key in controls["down"]:
                y = min(y + 1, 14)
        if key in controls["quit"]:
            exit()
        if key in controls["reset"]:
            return


if __name__ == "__main__":
    while True:
        wrapper(main)
