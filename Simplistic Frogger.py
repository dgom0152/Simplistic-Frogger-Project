import tkinter as tk

# Window settings
WIDTH = 600
HEIGHT = 700
CELL_SIZE = 50
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Colors
GREEN = "#3cb043"
BLUE = "#4da6ff"
GRAY = "#808080"
YELLOW = "#ffd84d"
RED = "#cc3333"
BROWN = "#8b5a2b"
WHITE = "#ffffff"
BLACK = "#000000"

# Game rows
GOAL_ROW = 0
WATER_ROWS = [1, 2, 3]
SAFE_ROWS = [4]
ROAD_ROWS = [5, 6, 7, 8]
START_ROW = 9

FROG_SIZE = 40
MOVE_STEP = CELL_SIZE

class FroggerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Frogger - Tkinter")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.message = None
        self.running = True
        self.win = False
        self.game_over = False

        self.frog_x = WIDTH // 2 - FROG_SIZE // 2
        self.frog_y = HEIGHT - CELL_SIZE + (CELL_SIZE - FROG_SIZE) // 2

        self.cars = [
            {"x": 100, "y": 5 * CELL_SIZE + 5, "w": 80, "h": 40, "speed": 4},
            {"x": 300, "y": 5 * CELL_SIZE + 5, "w": 80, "h": 40, "speed": 4},
            {"x": 200, "y": 6 * CELL_SIZE + 5, "w": 100, "h": 40, "speed": -5},
            {"x": 450, "y": 6 * CELL_SIZE + 5, "w": 100, "h": 40, "speed": -5},
            {"x": 50, "y": 7 * CELL_SIZE + 5, "w": 70, "h": 40, "speed": 6},
            {"x": 250, "y": 7 * CELL_SIZE + 5, "w": 70, "h": 40, "speed": 6},
            {"x": 150, "y": 8 * CELL_SIZE + 5, "w": 90, "h": 40, "speed": -3},
            {"x": 400, "y": 8 * CELL_SIZE + 5, "w": 90, "h": 40, "speed": -3},
        ]

        self.logs = [
            {"x": 50, "y": 1 * CELL_SIZE + 5, "w": 120, "h": 40, "speed": 2},
            {"x": 300, "y": 1 * CELL_SIZE + 5, "w": 120, "h": 40, "speed": 2},
            {"x": 100, "y": 2 * CELL_SIZE + 5, "w": 140, "h": 40, "speed": -3},
            {"x": 400, "y": 2 * CELL_SIZE + 5, "w": 140, "h": 40, "speed": -3},
            {"x": 0, "y": 3 * CELL_SIZE + 5, "w": 100, "h": 40, "speed": 4},
            {"x": 250, "y": 3 * CELL_SIZE + 5, "w": 100, "h": 40, "speed": 4},
        ]

        self.root.bind("<KeyPress>", self.on_key_press)

        self.update_game()

    def reset_game(self):
        self.running = True
        self.win = False
        self.game_over = False
        self.frog_x = WIDTH // 2 - FROG_SIZE // 2
        self.frog_y = HEIGHT - CELL_SIZE + (CELL_SIZE - FROG_SIZE) // 2

        self.cars = [
            {"x": 100, "y": 5 * CELL_SIZE + 5, "w": 80, "h": 40, "speed": 4},
            {"x": 300, "y": 5 * CELL_SIZE + 5, "w": 80, "h": 40, "speed": 4},
            {"x": 200, "y": 6 * CELL_SIZE + 5, "w": 100, "h": 40, "speed": -5},
            {"x": 450, "y": 6 * CELL_SIZE + 5, "w": 100, "h": 40, "speed": -5},
            {"x": 50, "y": 7 * CELL_SIZE + 5, "w": 70, "h": 40, "speed": 6},
            {"x": 250, "y": 7 * CELL_SIZE + 5, "w": 70, "h": 40, "speed": 6},
            {"x": 150, "y": 8 * CELL_SIZE + 5, "w": 90, "h": 40, "speed": -3},
            {"x": 400, "y": 8 * CELL_SIZE + 5, "w": 90, "h": 40, "speed": -3},
        ]

        self.logs = [
            {"x": 50, "y": 1 * CELL_SIZE + 5, "w": 120, "h": 40, "speed": 2},
            {"x": 300, "y": 1 * CELL_SIZE + 5, "w": 120, "h": 40, "speed": 2},
            {"x": 100, "y": 2 * CELL_SIZE + 5, "w": 140, "h": 40, "speed": -3},
            {"x": 400, "y": 2 * CELL_SIZE + 5, "w": 140, "h": 40, "speed": -3},
            {"x": 0, "y": 3 * CELL_SIZE + 5, "w": 100, "h": 40, "speed": 4},
            {"x": 250, "y": 3 * CELL_SIZE + 5, "w": 100, "h": 40, "speed": 4},
        ]

    def on_key_press(self, event):
        key = event.keysym.lower()

        if self.game_over or self.win:
            if key == "r":
                self.reset_game()
            return

        if key == "left":
            self.frog_x -= MOVE_STEP
        elif key == "right":
            self.frog_x += MOVE_STEP
        elif key == "up":
            self.frog_y -= MOVE_STEP
        elif key == "down":
            self.frog_y += MOVE_STEP

        self.frog_x = max(0, min(self.frog_x, WIDTH - FROG_SIZE))
        self.frog_y = max(0, min(self.frog_y, HEIGHT - FROG_SIZE))

    def draw_rows(self):
        for row in range(ROWS):
            y1 = row * CELL_SIZE
            y2 = y1 + CELL_SIZE

            if row == GOAL_ROW:
                color = YELLOW
            elif row in WATER_ROWS:
                color = BLUE
            elif row in SAFE_ROWS or row == START_ROW:
                color = GREEN
            elif row in ROAD_ROWS:
                color = GRAY
            else:
                color = BLACK

            self.canvas.create_rectangle(0, y1, WIDTH, y2, fill=color, outline=color)

    def move_objects(self):
        for car in self.cars:
            car["x"] += car["speed"]
            if car["speed"] > 0 and car["x"] > WIDTH:
                car["x"] = -car["w"]
            elif car["speed"] < 0 and car["x"] + car["w"] < 0:
                car["x"] = WIDTH

        for log in self.logs:
            log["x"] += log["speed"]
            if log["speed"] > 0 and log["x"] > WIDTH:
                log["x"] = -log["w"]
            elif log["speed"] < 0 and log["x"] + log["w"] < 0:
                log["x"] = WIDTH

    def rects_overlap(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return not (
            x1 + w1 <= x2 or
            x1 >= x2 + w2 or
            y1 + h1 <= y2 or
            y1 >= y2 + h2
        )

    def check_collisions(self):
        frog_row = self.frog_y // CELL_SIZE

        if frog_row == GOAL_ROW:
            self.win = True
            return

        if frog_row in ROAD_ROWS:
            for car in self.cars:
                if self.rects_overlap(
                    self.frog_x, self.frog_y, FROG_SIZE, FROG_SIZE,
                    car["x"], car["y"], car["w"], car["h"]
                ):
                    self.game_over = True
                    return

        if frog_row in WATER_ROWS:
            on_log = False

            for log in self.logs:
                if self.rects_overlap(
                    self.frog_x, self.frog_y, FROG_SIZE, FROG_SIZE,
                    log["x"], log["y"], log["w"], log["h"]
                ):
                    on_log = True
                    self.frog_x += log["speed"]
                    break

            if not on_log:
                self.game_over = True
                return

            if self.frog_x < 0 or self.frog_x + FROG_SIZE > WIDTH:
                self.game_over = True
                return

    def draw_objects(self):
        for car in self.cars:
            self.canvas.create_rectangle(
                car["x"], car["y"], car["x"] + car["w"], car["y"] + car["h"],
                fill=RED, outline=BLACK
            )

        for log in self.logs:
            self.canvas.create_rectangle(
                log["x"], log["y"], log["x"] + log["w"], log["y"] + log["h"],
                fill=BROWN, outline=BLACK
            )

        self.canvas.create_rectangle(
            self.frog_x, self.frog_y,
            self.frog_x + FROG_SIZE, self.frog_y + FROG_SIZE,
            fill=WHITE, outline=BLACK
        )

    def draw_message(self, text, color):
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text=text,
            fill=color,
            font=("Arial", 24, "bold")
        )

    def update_game(self):
        self.canvas.delete("all")
        self.draw_rows()

        if not self.game_over and not self.win:
            self.move_objects()
            self.check_collisions()

        self.draw_objects()

        if self.game_over:
            self.draw_message("Game Over! Press R", RED)
        elif self.win:
            self.draw_message("You Win! Press R", BLACK)

        self.root.after(100, self.update_game)

root = tk.Tk()
game = FroggerGame(root)
root.mainloop()