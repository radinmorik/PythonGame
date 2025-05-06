import pygame
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
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



############################################# Function: Read Card (Non-Blocking) #############################################
def read_card():
    """Try to read a card without blocking execution."""
    try:
        id, text = reader.read_no_block()  
        if id:
            id = hash(str(id))
            return str(id)  
    except Exception as e:
        print(f"RFID Error: {e}")
    return None  

############################################# Function: Authenticate User #############################################
def authenticateuser(user_id):
    """ Fetch user points from Firebase """
    user_ref = ref.child(user_id)
    user_data = user_ref.get()
    return user_data.get("points", 0) if user_data else 0  

############################################# Function: Update User Points #############################################
def update_user_points(user_id, points):
    """ Update user points in Firebase """
    user_ref = ref.child(user_id)
    user_ref.set({"points": round(points, 1)})  
    print(f"User {user_id} now has {points} points!")

############################################# Function: Add Leaf #############################################
def add_leaf(leaves, tree_x, tree_y, leaf_images):
    """ Try to add a leaf at a valid position on the tree """
    def is_valid_position(x, y, min_distance=25):
        for lx, ly, _ in leaves:
            if abs(lx - x) < min_distance and abs(ly - y) < min_distance:
                return False
        return True
    
    for _ in range(75):  
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
    if len(leaves) >= max_leaves:  
        leaves.clear()
        score += 0.1
        update_user_points(user_id, score)  
        return round(score,1), False  
    
    if add_leaf(leaves, tree_x, tree_y, leaf_images):
        score += 0.1
        update_user_points(user_id, score)
    
    add_leaf(leaves, tree_x, tree_y, leaf_images)
    add_leaf(leaves, tree_x, tree_y, leaf_images)
    
    
    
    return round(score,1), len(leaves) >= max_leaves  

############################################# Initialize pygame #############################################
pygame.init()

pygame.mixer.init()
click_sound = pygame.mixer.Sound("Click.wav")

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
score_tree = pygame.transform.scale(score_tree, (100, 100))
leaf_images = [pygame.transform.scale(leaf, (70, 70)) for leaf in leaf_images]

tree_x, tree_y = WIDTH // 2 - 150, HEIGHT // 2 - 200

# Game variables
leaves = []  
max_leaves = 27
font = pygame.font.Font(None, 69)
fontHeader = pygame.font.Font(None, 140)


tree_is_full = False  

# Button state tracking
last_button_state = True  

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

running = True
user_id = None  
score = 0

last_card_id = None
last_card_time = 0
CARD_COOLDOWN = 2

try:
    while running:
        screen.fill((0, 0, 0))

        # ======================== HANDLE LOGIN / LOGOUT ========================
        card_id = read_card()
        current_time = time.time()
        if card_id and (card_id != last_card_id or current_time - last_card_time > CARD_COOLDOWN):
            last_card_time = current_time
            last_card_id = card_id
            if user_id == card_id:  
                print(f"User {user_id} logged out!")
                user_id = None
                leaves.clear()
                score = 0
            else:  
                user_id = card_id
                score = authenticateuser(user_id)
                print(f"User {user_id} logged in! Current Score: {score}")

        # ======================== IDLE SCREEN ========================
        if user_id is None:              
            text = fontHeader.render("Welcome to Treecycle!", True, (0, 200, 0))
            screen.blit(text, (WIDTH // 2 - 550 + 40, 200))
            text = font.render("Tap card to Recycle!", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 3 + 40, HEIGHT // 2))
            pygame.display.flip()

        else:    
            text = fontHeader.render("Treecycle", True, (0, 200, 0))
            screen.blit(text, (WIDTH // 2 - 260 + 40, 100))
            
            text = font.render("Recycle in the Bin, then press the Button!", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 5 + 30, HEIGHT // 5 * 4 - 40))
            
            text = font.render("1 item = 1 press", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 4 + 220, HEIGHT // 9 * 8 - 50))
            
            text = font.render("Tap card again to Quit", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 3, HEIGHT // 9 * 8 + 30))
            
            input_state = GPIO.input(15)
            if input_state == False and last_button_state == True:
                click_sound.play()
                score, tree_is_full = handle_button_press(leaves, tree_x, tree_y, leaf_images, max_leaves, user_id, score)
            last_button_state = input_state  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            screen.blit(full_tree if tree_is_full else dead_tree, (tree_x, tree_y))

            for x, y, leaf in leaves:
                screen.blit(leaf, (x, y))

            screen.blit(score_tree, (WIDTH - 250, 30))
            score_text = font.render(f"{score}", True, (255, 255, 255))
            screen.blit(score_text, (WIDTH - 125, 60))

            pygame.display.flip()

        time.sleep(0.2)  

except KeyboardInterrupt:
    print("Game interrupted")
finally:
    GPIO.cleanup()
    pygame.quit()
    if user_id:
        update_user_points(user_id, score)
