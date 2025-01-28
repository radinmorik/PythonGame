import jellygame

window = jellygame.Window("game window")
window.create_grid(6, 6)

for x in range(0, 6):
    for y in range(0, 6):
        window.tiles[y][x].set_color(jellygame.color.GRAY)

for x in range(1, 5):
    for y in range(1, 5):
        window.tiles[y][x].set_color(jellygame.color.WHITE)


text1 = jellygame.Text("0", 5, 0, 1, 1, 24, background_color=jellygame.color.GRAY)
window.add_text(text1)

window.draw_grid(tile_size=100, show_grid=False)
window.start()
