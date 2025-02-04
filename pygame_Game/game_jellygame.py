import jellygame

window = jellygame.Window("game window")
window.create_grid(7, 7)


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

pieceGreen = jellygame.Jelly(jellygame.color.GREEN)
pieceBrown = jellygame.Jelly(jellygame.color.BROWN)

prog = 0

tiles = [window.tiles[1][3],
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

counter = 0

def handle_key_press(event=None):
    global prog
    global tiles
    global counter
    if prog == 0:
        window.tiles[5][3].set_jelly(pieceBrown)
        prog += 1
    elif prog <= 14:
        tiles[prog-1].set_jelly(pieceGreen)
        prog += 1
    else:
        clear_puzzle()
        counter += 1
        add_text()
        prog = 0
    window.draw_grid(tile_size=100, show_grid=True)


input_action = jellygame.InputAction(window, "a", handle_key_press)


def add_text():
    text1 = jellygame.Text(str(counter), 6, 0, 1, 1, 24, background_color=jellygame.color.GRAY)
    window.add_text(text1)


add_text()

window.draw_grid(tile_size=100, show_grid=True)
window.start()
