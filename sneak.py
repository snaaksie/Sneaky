import tkinter as tk
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
STEP_SIZE = 20

# Directions
UP, DOWN, LEFT, RIGHT = 'w', 's', 'a', 'd'
MOVEMENTS = {UP: (0, -STEP_SIZE), LEFT: (-STEP_SIZE, 0), DOWN: (0, STEP_SIZE), RIGHT: (STEP_SIZE, 0)}

# Initialize Window
window = tk.Tk()
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.title("Museum Stealth Game")

# Create Canvas
canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="gray20")
canvas.pack()

# Player
player = canvas.create_rectangle(40, 40, 60, 60, fill='black')

# Walls
walls = [
    canvas.create_rectangle(100, 100, 300, 120, fill='gray'),
    canvas.create_rectangle(400, 200, 600, 220, fill='gray'),
    canvas.create_rectangle(200, 300, 220, 500, fill='gray')
]

# Guards (Static for now)
guards = [
    canvas.create_rectangle(500, 100, 520, 120, fill='red'),
    canvas.create_rectangle(300, 400, 320, 420, fill='red')
]

# Exit
exit_zone = canvas.create_rectangle(700, 500, 780, 580, fill='green')

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
    
    # Check exit
    if check_collision((new_x1, new_y1, new_x2, new_y2), canvas.coords(exit_zone)):
        print("You escaped!")
        window.quit()
    
    canvas.move(player, x_move, y_move)

def check_collision(rect1, rect2):
    """Checks if two rectangles collide."""
    x1, y1, x2, y2 = rect1
    x3, y3, x4, y4 = rect2
    return not (x2 <= x3 or x1 >= x4 or y2 <= y3 or y1 >= y4)

# Bind keys
window.bind("<Key>", move_player)
window.mainloop()