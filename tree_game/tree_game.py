import pygame
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import time
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

############################################# Initialize Firebase #############################################
cred = credentials.Certificate("/home/shvan/Downloads/treegame-b8ae6-firebase-adminsdk-fbsvc-8c07c43e75.json")
default_app = firebase_admin.initialize_app(cred, {
   'databaseURL': 'https://treegame-b8ae6-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference("/")

reader = SimpleMFRC522()

def authenticateuser():
    """ Wait for the user to tap a card and return the user ID and existing points """
    
    print("Hold a tag near the reader to start the game.")

    while True:
        try:
            id, text = reader.read()  # This returns both ID and text
            user_id = str(id)  # Convert to string
            
            # Get user data from Firebase
            user_ref = ref.child(user_id)
            user_data = user_ref.get()
            current_points = user_data.get("points", 0) if user_data else 0
            
            print(f"Welcome, User {user_id}! You have {current_points} points.")
            return user_id, current_points  # Return authenticated user ID and their points

        except KeyboardInterrupt:
            GPIO.cleanup()
            print("Error! (Noe gikk galt)")    
            sys.exit(1)

############################################# Function: Update User Points #############################################
def update_user_points(user_id, points):
    """ Update user points in Firebase with the current score """
    user_ref = ref.child(user_id)
    points = round(points, 1)  # Round to one decimal place
    user_ref.set({"points": points})  # Update Firebase
    print(f"User {user_id} now has {points} points!")

############################################# Function: Add Leaf #############################################
def add_leaf(leaves, tree_x, tree_y, leaf_images):
    """ Try to add a leaf at a valid position on the tree """
    def is_valid_position(x, y, min_distance=25):
        for lx, ly, _ in leaves:
            if abs(lx - x) < min_distance and abs(ly - y) < min_distance:
                return False
        return True
    
    for _ in range(75):  # Try multiple times to find a valid position
        x_offset = random.randint(17, 220)
        y_offset = random.randint(17, 200)
        new_x, new_y = tree_x + x_offset, tree_y + y_offset
        if is_valid_position(new_x, new_y):
            leaf = random.choice(leaf_images)
            leaves.append((new_x, new_y, leaf))
            return True
    return False

############################################# Function: Handle Button Press #############################################
def handle_button_press(leaves, tree_x, tree_y, leaf_images, max_leaves, user_id, score):
    """ Handle tree growth when button is pressed """
    if len(leaves) >= max_leaves:  # Tree is full
        leaves.clear()
        update_user_points(user_id, score)
        return score, False  # Reset tree_is_full flag
    
    if add_leaf(leaves, tree_x, tree_y, leaf_images):
        score += 0.1
        score = round(score, 1)
        update_user_points(user_id, score)
    
    # Try to add 2 more leaves for visual effect
    add_leaf(leaves, tree_x, tree_y, leaf_images)
    add_leaf(leaves, tree_x, tree_y, leaf_images)
    
    tree_is_full = len(leaves) >= max_leaves
    if tree_is_full:
        update_user_points(user_id, score)
    
    return score, tree_is_full

############################################# Initialize pygame #############################################
pygame.init()

# Get actual screen dimensions
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Tree Growth Game")

# Load images
dead_tree = pygame.image.load("dead_tree.png")
full_tree = pygame.image.load("full_tree.png")
score_tree = pygame.image.load("full_tree.png")
leaf_images = [
    pygame.image.load("leaf1.png"),
    pygame.image.load("leaf2.png"),
    pygame.image.load("leaf3.png"),
]

# Resize images
dead_tree = pygame.transform.scale(dead_tree, (300, 400))
full_tree = pygame.transform.scale(full_tree, (300, 400))
score_tree = pygame.transform.scale(score_tree, (40, 40))
leaf_images = [pygame.transform.scale(leaf, (70, 70)) for leaf in leaf_images]

# Tree position (center it based on actual screen dimensions)
tree_x, tree_y = WIDTH // 2 - 150, HEIGHT // 2 - 200

# Auth user before starting and get their current points
user_id, score = authenticateuser()

# Game variables
leaves = []  # Stores (x, y, image) for each leaf
max_leaves = 30
font = pygame.font.Font(None, 36)
tree_is_full = False  # Tracks whether the tree is fully grown

# Add key to exit game
print("Press ESC to exit the game")
print("Press the physical button on GPIO 15 to grow the tree")






# Button state tracking
last_button_state = True  # Pull-up means default is True (not pressed)

# Ensure GPIO setup is correct before the loop | Doesnt work if it s not here aswell
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)


running = True
try:
    while running:
        # :one: Check PHYSICAL BUTTON before anything else
        input_state = GPIO.input(15)
        if input_state == False and last_button_state == True:  # Button just pressed
            #print(":rocket: Physical button pressed!")
            score, tree_is_full = handle_button_press(leaves, tree_x, tree_y, leaf_images, max_leaves, user_id, score)
        last_button_state = input_state  # Update last state

        # :two: Handle Pygame Events (Keyboard & Mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button_x <= mx <= button_x + button_w and button_y <= my <= button_y + button_h:
                    print(":mouse_three_button: Mouse button clicked!")
                    score, tree_is_full = handle_button_press(leaves, tree_x, tree_y, leaf_images, max_leaves, user_id, score)

        # :three: Draw everything
        screen.fill((0, 0, 0))
        screen.blit(full_tree if tree_is_full else dead_tree, (tree_x, tree_y))

        # Draw leaves
        for x, y, leaf in leaves:
            screen.blit(leaf, (x, y))

        # Draw score
        screen.blit(score_tree, (WIDTH - 100, 20))
        score_text = font.render(f"{score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 50, 30))

    

        pygame.display.flip()

        # :four: Reduce sleep time to prevent missed inputs
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Game interrupted")
finally:
    GPIO.cleanup()
    pygame.quit()
    update_user_points(user_id, score)

