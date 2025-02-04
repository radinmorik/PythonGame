import jellygame

window = jellygame.Window("game window")
window.create_grid(7, 7)


def create_frame():
    for x in range(0, 7):
        for y in range(0, 7):
            window.tiles[y][x].set_color(jellygame.color.GRAY)
    for x in range(1, 6):
        for y in range(1, 6):
            window.tiles[y][x].set_color(jellygame.color.WHITE)


def clear_puzzle():
    for x in range(1, 6):
        for y in range(1, 6):
            window.tiles[y][x].set_jelly(None)


def draw_text():
    text1.set_text(str(counter))
    window.add_text(text1)


def handle_key_press(event=None):
    global prog
    global tiles
    global counter
    if prog == 0:
        window.tiles[5][3].set_jelly(piece_brown)
        prog += 1
    elif prog <= 14:
        green_tiles[prog-1].set_jelly(piece_green)
        prog += 1
    else:
        clear_puzzle()
        counter += 1
        draw_text()
        prog = 0
    window.draw_grid(tile_size=100, show_grid=True)


# Parameters
piece_green = jellygame.Jelly(jellygame.color.GREEN)
piece_brown = jellygame.Jelly(jellygame.color.BROWN)

prog = 0
counter = 0

green_tiles = [window.tiles[1][3],
               window.tiles[2][2],
               window.tiles[2][3],
               window.tiles[2][4],
               window.tiles[3][1],
               window.tiles[3][2],
               window.tiles[3][3],
               window.tiles[3][4],
               window.tiles[3][5],
               window.tiles[4][1],
               window.tiles[4][2],
               window.tiles[4][3],
               window.tiles[4][4],
               window.tiles[4][5]]


create_frame()

input_action = jellygame.InputAction(window, "a", handle_key_press)

text1 = jellygame.Text(str(counter), 6, 0, 1, 1, 24, background_color=jellygame.color.GRAY)
draw_text()

window.draw_grid(tile_size=100, show_grid=True)
window.start()
