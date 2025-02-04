import jellygame

window = jellygame.Window("game window")
window.create_grid(6, 6)

for x in range(0, 6):
    for y in range(0, 6):
        window.tiles[y][x].set_color(jellygame.color.GRAY)

for x in range(1, 5):
    for y in range(1, 5):
        window.tiles[y][x].set_color(jellygame.color.WHITE)


sprite = jellygame.Sprite("Sprites/tree_dead.png")
jelly = jellygame.Jelly(color=jellygame.color.GRAY, sprite=sprite)
window.tiles[0][4].set_jelly(jelly)

window.draw_canvas(tile_size=100)
sprite.draw_sprite(window.get_canvas(), 12, 0)
window.start()
