import tkinter as tk
import random

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
STEP_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // STEP_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // STEP_SIZE

# Directions
UP, DOWN, LEFT, RIGHT = (0, -STEP_SIZE), (0, STEP_SIZE), (-STEP_SIZE, 0), (STEP_SIZE, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Initialize Window
window = tk.Tk()
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.title("Stealth Game")

# Create Canvas
canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="gray20")
canvas.pack()

# Helper functions
def check_collision(rect1, rect2):
    x1, y1, x2, y2 = rect1
    x3, y3, x4, y4 = rect2
    return not (x2 <= x3 or x1 >= x4 or y2 <= y3 or y1 >= y4)

def get_random_position(occupied, width=STEP_SIZE, height=STEP_SIZE):
    while True:
        x = random.randint(0, GRID_WIDTH - 1) * STEP_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * STEP_SIZE
        if all(not check_collision((x, y, x + width, y + height), pos) for pos in occupied):
            occupied.append((x, y, x + width, y + height))
            return x, y

occupied_positions = []

# Player
px, py = get_random_position(occupied_positions)
player = canvas.create_rectangle(px, py, px + STEP_SIZE, py + STEP_SIZE, fill='black')

# Walls
walls = []
for _ in range(10):
    width_modifier = random.randint(3, 10)
    wx, wy = get_random_position(occupied_positions, width=STEP_SIZE * width_modifier, height=STEP_SIZE)
    walls.append(canvas.create_rectangle(wx, wy, wx + STEP_SIZE * width_modifier, wy + STEP_SIZE, fill='gray'))

# Guard System
guards = []
guard_paths = {}
guard_indices = {}

def create_guard():
    gx, gy = get_random_position(occupied_positions)
    guard = canvas.create_rectangle(gx, gy, gx + STEP_SIZE, gy + STEP_SIZE, fill='red')
    guards.append(guard)
    
    # Generate random patrol waypoints
    path = [(gx, gy)]
    for _ in range(random.randint(3, 6)):
        dx, dy = random.choice(DIRECTIONS)
        new_x, new_y = path[-1][0] + dx * random.randint(3, 6), path[-1][1] + dy * random.randint(3, 6)
        new_x = max(0, min(WINDOW_WIDTH - STEP_SIZE, new_x))
        new_y = max(0, min(WINDOW_HEIGHT - STEP_SIZE, new_y))
        path.append((new_x, new_y))
    
    guard_paths[guard] = path
    guard_indices[guard] = 0
    move_guard(guard)

def move_guard(guard):
    path = guard_paths[guard]
    index = guard_indices[guard]
    target_x, target_y = path[index]
    gx, gy = canvas.coords(guard)[:2]
    
    dx = STEP_SIZE if gx < target_x else -STEP_SIZE if gx > target_x else 0
    dy = STEP_SIZE if gy < target_y else -STEP_SIZE if gy > target_y else 0
    
    # Move guard smoothly
    if (gx, gy) != (target_x, target_y):
        canvas.move(guard, dx, dy)
        window.after(200, move_guard, guard)
    else:
        guard_indices[guard] = (index + 1) % len(path)  # Move to next waypoint
        window.after(1000, move_guard, guard)  # Pause before moving

def detect_player():
    px1, py1, px2, py2 = canvas.coords(player)
    for guard in guards:
        gx1, gy1, gx2, gy2 = canvas.coords(guard)
        
        # Guard sees the player in a straight line
        if px1 == gx1 or py1 == gy1:
            obstructed = any(check_collision((px1, py1, px2, py2), canvas.coords(wall)) for wall in walls)
            if not obstructed:
                canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="GAME OVER", fill="white", font=("Arial", 40))
                return
    window.after(200, detect_player)

# Create Guards
for _ in range(5):
    create_guard()
detect_player()

# Player movement
def move_player(event):
    key_map = {'w': UP, 's': DOWN, 'a': LEFT, 'd': RIGHT}
    if event.char not in key_map:
        return
    
    x_move, y_move = key_map[event.char]
    x1, y1, x2, y2 = canvas.coords(player)
    new_x1, new_y1, new_x2, new_y2 = x1 + x_move, y1 + y_move, x2 + x_move, y2 + y_move
    
    # Check wall collision
    if any(check_collision((new_x1, new_y1, new_x2, new_y2), canvas.coords(wall)) for wall in walls):
        return
    
    canvas.move(player, x_move, y_move)

# Bind keys
window.bind("<Key>", move_player)
window.mainloop()
