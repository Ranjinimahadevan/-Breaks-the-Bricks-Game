import tkinter as tk
import random

# Set up the main window
window = tk.Tk()
window.title("Break the Brick Game")
window.resizable(0, 0)

canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Paddle
paddle = canvas.create_rectangle(350, 580, 450, 590, fill="blue")
paddle_speed = 20

# Ball
ball = canvas.create_oval(390, 570, 410, 590, fill="red")
ball_dx = 4
ball_dy = -4

# Bricks
brick_rows = 5
brick_cols = 10
brick_width = 75
brick_height = 20
bricks = []

for i in range(brick_rows):
    for j in range(brick_cols):
        x1 = j * (brick_width + 5) + 30
        y1 = i * (brick_height + 5) + 30
        x2 = x1 + brick_width
        y2 = y1 + brick_height
        brick = canvas.create_rectangle(x1, y1, x2, y2, fill="green")
        bricks.append(brick)

# Move paddle with arrow keys
def move_left(event):
    x1, y1, x2, y2 = canvas.coords(paddle)
    if x1 > 0:
        canvas.move(paddle, -paddle_speed, 0)

def move_right(event):
    x1, y1, x2, y2 = canvas.coords(paddle)
    if x2 < canvas_width:
        canvas.move(paddle, paddle_speed, 0)

window.bind("<Left>", move_left)
window.bind("<Right>", move_right)

# Game over / Win message
def display_message(text):
    canvas.create_text(canvas_width / 2, canvas_height / 2, text=text, fill="white", font=("Arial", 30))

# Main game loop
def update_game():
    global ball_dx, ball_dy

    canvas.move(ball, ball_dx, ball_dy)
    ball_coords = canvas.coords(ball)
    paddle_coords = canvas.coords(paddle)

    # Wall collision
    if ball_coords[0] <= 0 or ball_coords[2] >= canvas_width:
        ball_dx = -ball_dx
    if ball_coords[1] <= 0:
        ball_dy = -ball_dy

    # Paddle collision
    if (paddle_coords[0] < ball_coords[2] < paddle_coords[2] or paddle_coords[0] < ball_coords[0] < paddle_coords[2]) \
            and paddle_coords[1] <= ball_coords[3] <= paddle_coords[3]:
        ball_dy = -ball_dy

    # Brick collision
    for brick in bricks:
        brick_coords = canvas.coords(brick)
        if brick_coords:
            if (brick_coords[0] < ball_coords[2] and ball_coords[0] < brick_coords[2]) and \
               (brick_coords[1] < ball_coords[3] and ball_coords[1] < brick_coords[3]):
                canvas.delete(brick)
                bricks.remove(brick)
                ball_dy = -ball_dy
                break

    # Win check
    if not bricks:
        display_message("You Win!")
        return

    # Lose check
    if ball_coords[3] >= canvas_height:
        display_message("Game Over!")
        return

    window.after(20, update_game)

# Start the game loop
update_game()
window.mainloop()
