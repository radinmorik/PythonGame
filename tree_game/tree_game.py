import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Tree Growth Game")

# Load images
dead_tree = pygame.image.load("dead_tree.png")
full_tree = pygame.image.load("full_tree.png")
score_tree = pygame.image.load("full_tree.png")
leaf_images = [
    pygame.image.load("leaf1.png"),  # Replace with correct file names
    pygame.image.load("leaf2.png"),
    pygame.image.load("leaf3.png"),
]

# Resize images
dead_tree = pygame.transform.scale(dead_tree, (300, 400))
full_tree = pygame.transform.scale(full_tree, (300, 400))
score_tree = pygame.transform.scale(score_tree, (40, 40))
leaf_images = [pygame.transform.scale(leaf, (70, 70)) for leaf in leaf_images]

# Tree position
tree_x, tree_y = WIDTH // 2 - 150, HEIGHT // 2 - 200

# Game variables
leaves = []  # Stores (x, y, image) for each leaf
max_leaves = 35
score = 0
font = pygame.font.Font(None, 36)
button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 80, 100, 50)
tree_is_full = False  # Tracks whether the tree is fully grown

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tree_is_full:
                leaves.clear()  # Remove all leaves when the full tree appears
                tree_is_full = False

            def is_valid_position(x, y, min_distance=25):
                for lx, ly, _ in leaves:
                    if abs(lx - x) < min_distance and abs(ly - y) < min_distance:
                        return False
                return True


            if len(leaves) < max_leaves:
                for _ in range(75):  # Try multiple times to find a valid position
                    x_offset = random.randint(17, 220)
                    y_offset = random.randint(17, 200)
                    new_x, new_y = tree_x + x_offset, tree_y + y_offset
                    if is_valid_position(new_x, new_y):
                        leaf = random.choice(leaf_images)
                        leaves.append((new_x, new_y, leaf))
                        break

                if len(leaves) >= max_leaves:
                    score += 1
                    tree_is_full = True  # Mark the tree as full

            if len(leaves) < max_leaves:
                for _ in range(75):  # Try multiple times to find a valid position
                    x_offset = random.randint(17, 220)
                    y_offset = random.randint(17, 200)
                    new_x, new_y = tree_x + x_offset, tree_y + y_offset
                    if is_valid_position(new_x, new_y):
                        leaf = random.choice(leaf_images)
                        leaves.append((new_x, new_y, leaf))
                        break

                if len(leaves) >= max_leaves:
                    score += 1
                    tree_is_full = True  # Mark the tree as full

            if len(leaves) < max_leaves:
                for _ in range(75):  # Try multiple times to find a valid position
                    x_offset = random.randint(17, 220)
                    y_offset = random.randint(17, 200)
                    new_x, new_y = tree_x + x_offset, tree_y + y_offset
                    if is_valid_position(new_x, new_y):
                        leaf = random.choice(leaf_images)
                        leaves.append((new_x, new_y, leaf))
                        break

                if len(leaves) >= max_leaves:
                    score += 1
                    tree_is_full = True  # Mark the tree as full

    # Draw tree
    if len(leaves) >= max_leaves:
        screen.blit(full_tree, (tree_x, tree_y))

    else:
        screen.blit(dead_tree, (tree_x, tree_y))

    # Draw leaves
    for x, y, leaf in leaves:
        screen.blit(leaf, (x, y))

    # Draw button
    pygame.draw.rect(screen, (100, 200, 100), button_rect)
    button_text = font.render("Grow", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 15))

    # 🎯 Draw mini tree icon + score text
    screen.blit(score_tree, (WIDTH - 100, 20))  # Position icon
    score_text = font.render(f"{score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 50, 30))  # Position number next to icon

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
