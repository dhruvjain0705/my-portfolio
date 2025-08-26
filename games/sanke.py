import tkinter as tk
import random

# Game settings
GAME_WIDTH = 600
GAME_HEIGHT = 400
SPEED = 150   # milliseconds per move
SPACE_SIZE = 20
SNAKE_COLOR = "green"
APPLE_COLOR = "red"
BACKGROUND_COLOR = "black"
BORDER_COLOR = "blue"

class Snake:
    def __init__(self, canvas):
        self.body_size = 3
        self.coordinates = []
        self.squares = []

        for i in range(0, self.body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)

class Apple:
    def __init__(self, canvas):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=APPLE_COLOR, tag="apple"
        )

def next_turn(snake, apple):
    global running, score

    if not running:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    if x == apple.coordinates[0] and y == apple.coordinates[1]:
        canvas.delete("apple")
        apple = Apple(canvas)
        score += 1
        label.config(text=f"Score: {score}")
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, apple)

def change_direction(new_direction):
    global direction
    if new_direction == "left" and direction != "right":
        direction = "left"
    elif new_direction == "right" and direction != "left":
        direction = "right"
    elif new_direction == "up" and direction != "down":
        direction = "up"
    elif new_direction == "down" and direction != "up":
        direction = "down"

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    global running
    running = False
    canvas.delete("all")
    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 - 20,
        text="GAME OVER",
        fill="red",
        font=("Arial", 30, "bold"),
    )
    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 + 20,
        text=f"Final Score: {score}",
        fill="white",
        font=("Arial", 20, "bold"),
    )
    restart_btn.pack(pady=10)

def restart_game():
    global snake, apple, direction, running, score
    canvas.delete("all")
    restart_btn.pack_forget()
    direction = "right"
    running = True
    score = 0
    label.config(text=f"Score: {score}")
    snake = Snake(canvas)
    apple = Apple(canvas)
    next_turn(snake, apple)

# --- Main program ---
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

# Score label
label = tk.Label(window, text="Score: 0", font=("Arial", 14), bg="black", fg="white")
label.pack()

# Canvas
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH,
                   highlightthickness=5, highlightbackground=BORDER_COLOR)
canvas.pack()

direction = "right"
running = True
score = 0

snake = Snake(canvas)
apple = Apple(canvas)

# Control buttons
frame = tk.Frame(window, bg=BACKGROUND_COLOR)
frame.pack()

btn_up = tk.Button(frame, text="↑ Up", command=lambda: change_direction("up"), bg="blue", fg="white", width=8)
btn_up.grid(row=0, column=1)

btn_left = tk.Button(frame, text="← Left", command=lambda: change_direction("left"), bg="blue", fg="white", width=8)
btn_left.grid(row=1, column=0)

btn_down = tk.Button(frame, text="↓ Down", command=lambda: change_direction("down"), bg="blue", fg="white", width=8)
btn_down.grid(row=1, column=1)

btn_right = tk.Button(frame, text="→ Right", command=lambda: change_direction("right"), bg="blue", fg="white", width=8)
btn_right.grid(row=1, column=2)

# Restart button (hidden until game over)
restart_btn = tk.Button(window, text="Restart", command=restart_game, bg="red", fg="white", width=10)

# Keyboard controls
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))

# Start game
next_turn(snake, apple)

window.mainloop()
