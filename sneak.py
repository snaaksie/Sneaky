import tkinter as tk
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
STEP_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // STEP_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // STEP_SIZE

# Directions
UP, DOWN, LEFT, RIGHT = 'w', 's', 'a', 'd'
MOVEMENTS = {UP: (0, -STEP_SIZE), LEFT: (-STEP_SIZE, 0), DOWN: (0, STEP_SIZE), RIGHT: (STEP_SIZE, 0)}
PATROL_PATHS = [[(STEP_SIZE, 0), (STEP_SIZE, 0), (-STEP_SIZE, 0), (-STEP_SIZE, 0)],
                [(0, STEP_SIZE), (0, -STEP_SIZE)]]

# Initialize Window
window = tk.Tk()
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.title("Sneak Game")

# Create Canvas
canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="gray20")
canvas.pack()

# Helper functions
def get_random_position(occupied, width=STEP_SIZE, height=STEP_SIZE):
    while True:
        x = random.randint(0, GRID_WIDTH - 1) * STEP_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * STEP_SIZE
        if all(not check_collision((x, y, x + width, y + height), pos) for pos in occupied):
            occupied.append((x, y, x + width, y + height))
            return x, y

def check_collision(rect1, rect2):
    x1, y1, x2, y2 = rect1
    x3, y3, x4, y4 = rect2
    return not (x2 <= x3 or x1 >= x4 or y2 <= y3 or y1 >= y4)

# Store occupied positions
occupied_positions = []

# Player
px, py = get_random_position(occupied_positions)
player = canvas.create_rectangle(px, py, px + STEP_SIZE, py + STEP_SIZE, fill='black')

# Walls
walls = []
for _ in range(5):  # Create 5 random walls
    width_modifier = random.randint(3, 10)
    wx, wy = get_random_position(occupied_positions, width=STEP_SIZE * width_modifier, height=STEP_SIZE)
    walls.append(canvas.create_rectangle(wx, wy, wx + STEP_SIZE * width_modifier, wy + STEP_SIZE, fill='gray'))

# Guards with movement
guards = []
guard_paths = {}
guard_indices = {}

def move_guard(guard):
    path = guard_paths[guard]
    index = guard_indices[guard]
    direction = path[index]
    
    x1, y1, x2, y2 = canvas.coords(guard)
    new_x1, new_y1, new_x2, new_y2 = x1 + direction[0], y1 + direction[1], x2 + direction[0], y2 + direction[1]
    
    # Check collision with walls
    for wall in walls:
        if check_collision((new_x1, new_y1, new_x2, new_y2), canvas.coords(wall)):
            return  # Stop movement if collides
    
    canvas.move(guard, direction[0], direction[1])
    guard_indices[guard] = (index + 1) % len(path)  # Loop through path
    window.after(500, move_guard, guard)  # Repeat movement

# Create 2 guards with path movement
for _ in range(3):
    gx, gy = get_random_position(occupied_positions)
    guard = canvas.create_rectangle(gx, gy, gx + STEP_SIZE, gy + STEP_SIZE, fill='red')
    guards.append(guard)
    path = random.choice(PATROL_PATHS)
    guard_paths[guard] = path
    guard_indices[guard] = 0
    move_guard(guard)

# Player movement
def move_player(event):
    """Moves the player while checking for collisions."""
    if event.char not in MOVEMENTS:
        return
    
    x_move, y_move = MOVEMENTS[event.char]
    x1, y1, x2, y2 = canvas.coords(player)
    new_x1, new_y1, new_x2, new_y2 = x1 + x_move, y1 + y_move, x2 + x_move, y2 + y_move
    
    # Check wall collision
    for wall in walls:
        if check_collision((new_x1, new_y1, new_x2, new_y2), canvas.coords(wall)):
            return
    
    canvas.move(player, x_move, y_move)

# Bind keys
window.bind("<Key>", move_player)
window.mainloop()
