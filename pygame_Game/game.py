import tkinter as tk
from PIL import Image, ImageTk

# Puzzle settings
grid_size = 6
puzzle_size = 4
tile_size = 36  # Adjust as needed
image_path = "tree.png"  # Change to your image

# Initialize main Tkinter window
root = tk.Tk()
root.title("4x4 Image Puzzle")

# Load and split the image
img = Image.open(image_path)
img = img.resize((puzzle_size * tile_size, puzzle_size * tile_size))

# Save the full image for the preview at (5,0)
full_image = ImageTk.PhotoImage(img)

# Create the tile pieces
tiles = []
for i in range(puzzle_size):
    row_tiles = []
    for j in range(puzzle_size):
        tile = img.crop((j * tile_size, i * tile_size, (j + 1) * tile_size, (i + 1) * tile_size))
        row_tiles.append(ImageTk.PhotoImage(tile))
    tiles.append(row_tiles)

# Create a 6x6 grid of buttons
buttons = [[None for _ in range(grid_size)] for _ in range(grid_size)]
revealed = [[False for _ in range(grid_size)] for _ in range(grid_size)]
completion_count = 0  # Track puzzle completions

# Function to reveal the tile
def reveal_tile(row, col):
    global completion_count
    if not revealed[row][col]:
        buttons[row][col].config(image=tiles[row][col])  # Reveal the image piece
        revealed[row][col] = True
        check_completion()

# Function to check puzzle completion
def check_completion():
    global completion_count
    if all(revealed[row][col] for row in range(1, 5) for col in range(1, 5)):  # Check 4x4 grid
        completion_count += 1
        counter_label.config( {completion_count})
        reset_puzzle()

# Function to reset the puzzle
def reset_puzzle():
    for row in range(1, 5):
        for col in range(1, 5):
            buttons[row][col].config(image="", text="")  # Reset image
            revealed[row][col] = False

# Create buttons for the 4x4 puzzle grid
for row in range(grid_size):
    for col in range(grid_size):
        if 1 <= row <= 4 and 1 <= col <= 4:  # Only the 4x4 puzzle area
            btn = tk.Button(root, width=10, height=5, command=lambda r=row, c=col: reveal_tile(r, c))
            btn.grid(row=row, column=col, padx=1, pady=1)
            buttons[row][col] = btn
        else:  # Create non-clickable labels for the rest of the grid
            label = tk.Label(root, text=" ", width=10, height=5, relief="solid")
            label.grid(row=row, column=col, padx=1, pady=1)

max_width = 50;
max_height = 50  # Maximum height

# Resize the image to fit within the max width and height, maintaining the aspect ratio
full_image_resized = img.copy()  # Make a copy to avoid modifying the original image
full_image_resized.thumbnail((max_width, max_height))  # Resize while maintaining aspect ratio

# Convert resized image to PhotoImage object for Tkinter
full_image_resized_tk = ImageTk.PhotoImage(full_image_resized)

# Add the resized full-image preview at (5,0)
full_image_label = tk.Label(root, image=full_image_resized_tk)
full_image_label.grid(row=0, column=4, rowspan=1, columnspan=1)

# Add a counter at (6,0)
counter_label = tk.Label(root, text=f" {completion_count}", font=("Arial", 14, "bold"))
counter_label.grid(row=0, column=5, columnspan=1)

# Run the application
root.mainloop()
