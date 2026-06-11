import tkinter as tk

# -----------------------------
# GAME SETTINGS
# -----------------------------
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
CELL_SIZE = 50

ROWS = WINDOW_HEIGHT // CELL_SIZE
COLUMNS = WINDOW_WIDTH // CELL_SIZE

FROG_SIZE = 40
FROG_MOVE_DISTANCE = CELL_SIZE
GAME_SPEED_MS = 100  # lower number = faster game updates

# -----------------------------
# COLORS
# -----------------------------
COLOR_GRASS = "#3cb043"
COLOR_WATER = "#4da6ff"
COLOR_ROAD = "#808080"
COLOR_GOAL = "#ffd84d"
COLOR_CAR = "#cc3333"
COLOR_LOG = "#8b5a2b"
COLOR_FROG = "#ffffff"
COLOR_BLACK = "#000000"

# -----------------------------
# ROW DEFINITIONS
# -----------------------------
GOAL_ROW = 0
WATER_ROWS = [1, 2, 3]
SAFE_ROWS = [4]
ROAD_ROWS = [5, 6, 7, 8]
START_ROW = 9


class FroggerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simplitic Frogger - Code In Place Project - Dexter Gomez")

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=COLOR_BLACK
        )
        self.canvas.pack()

        # Set up the game for the first time
        self.setup_game()

        # Listen for keyboard input
        self.root.bind("<KeyPress>", self.handle_key_press)

        # Start the game loop
        self.update_game()

    def setup_game(self):
        """Set starting values for the frog, cars, logs, and game state."""
        self.has_won = False
        self.is_game_over = False

        self.reset_frog_position()
        self.create_cars()
        self.create_logs()

    def reset_frog_position(self):
        """Place the frog in the starting row."""
        self.frog_x = WINDOW_WIDTH // 2 - FROG_SIZE // 2
        self.frog_y = WINDOW_HEIGHT - CELL_SIZE + (CELL_SIZE - FROG_SIZE) // 2

    def create_cars(self):
        """Create all car objects."""
        self.cars = [
            {"x": 100, "y": 5 * CELL_SIZE + 5, "width": 80, "height": 40, "speed": 4},
            {"x": 300, "y": 5 * CELL_SIZE + 5, "width": 80, "height": 40, "speed": 4},
            {"x": 200, "y": 6 * CELL_SIZE + 5, "width": 100, "height": 40, "speed": -5},
            {"x": 450, "y": 6 * CELL_SIZE + 5, "width": 100, "height": 40, "speed": -5},
            {"x": 50, "y": 7 * CELL_SIZE + 5, "width": 70, "height": 40, "speed": 6},
            {"x": 250, "y": 7 * CELL_SIZE + 5, "width": 70, "height": 40, "speed": 6},
            {"x": 150, "y": 8 * CELL_SIZE + 5, "width": 90, "height": 40, "speed": -3},
            {"x": 400, "y": 8 * CELL_SIZE + 5, "width": 90, "height": 40, "speed": -3},
        ]

    def create_logs(self):
        """Create all log objects."""
        self.logs = [
            {"x": 50, "y": 1 * CELL_SIZE + 5, "width": 120, "height": 40, "speed": 2},
            {"x": 300, "y": 1 * CELL_SIZE + 5, "width": 120, "height": 40, "speed": 2},
            {"x": 100, "y": 2 * CELL_SIZE + 5, "width": 140, "height": 40, "speed": -3},
            {"x": 400, "y": 2 * CELL_SIZE + 5, "width": 140, "height": 40, "speed": -3},
            {"x": 0, "y": 3 * CELL_SIZE + 5, "width": 100, "height": 40, "speed": 4},
            {"x": 250, "y": 3 * CELL_SIZE + 5, "width": 100, "height": 40, "speed": 4},
        ]

    def reset_game(self):
        """Restart the whole game."""
        self.setup_game()

    def handle_key_press(self, event):
        """Move the frog when the player presses an arrow key."""
        key_pressed = event.keysym.lower()

        # If game has ended, only allow restart
        if self.is_game_over or self.has_won:
            if key_pressed == "r":
                self.reset_game()
            return

        if key_pressed == "left":
            self.frog_x -= FROG_MOVE_DISTANCE
        elif key_pressed == "right":
            self.frog_x += FROG_MOVE_DISTANCE
        elif key_pressed == "up":
            self.frog_y -= FROG_MOVE_DISTANCE
        elif key_pressed == "down":
            self.frog_y += FROG_MOVE_DISTANCE

        self.keep_frog_inside_window()

    def keep_frog_inside_window(self):
        """Make sure the frog cannot move off the screen."""
        self.frog_x = max(0, min(self.frog_x, WINDOW_WIDTH - FROG_SIZE))
        self.frog_y = max(0, min(self.frog_y, WINDOW_HEIGHT - FROG_SIZE))

    def draw_background_rows(self):
        """Draw the colored rows for goal, water, safe area, road, and start."""
        for row in range(ROWS):
            top_y = row * CELL_SIZE
            bottom_y = top_y + CELL_SIZE

            if row == GOAL_ROW:
                row_color = COLOR_GOAL
            elif row in WATER_ROWS:
                row_color = COLOR_WATER
            elif row in SAFE_ROWS or row == START_ROW:
                row_color = COLOR_GRASS
            elif row in ROAD_ROWS:
                row_color = COLOR_ROAD
            else:
                row_color = COLOR_BLACK

            self.canvas.create_rectangle(
                0, top_y,
                WINDOW_WIDTH, bottom_y,
                fill=row_color,
                outline=row_color
            )

    def move_cars(self):
        """Move every car across the screen."""
        for car in self.cars:
            car["x"] += car["speed"]

            # If a car moves off one side, wrap it to the other side
            if car["speed"] > 0 and car["x"] > WINDOW_WIDTH:
                car["x"] = -car["width"]
            elif car["speed"] < 0 and car["x"] + car["width"] < 0:
                car["x"] = WINDOW_WIDTH

    def move_logs(self):
        """Move every log across the screen."""
        for log in self.logs:
            log["x"] += log["speed"]

            # If a log moves off one side, wrap it to the other side
            if log["speed"] > 0 and log["x"] > WINDOW_WIDTH:
                log["x"] = -log["width"]
            elif log["speed"] < 0 and log["x"] + log["width"] < 0:
                log["x"] = WINDOW_WIDTH

    def move_all_objects(self):
        """Move cars and logs each game update."""
        self.move_cars()
        self.move_logs()

    def rectangles_overlap(self, x1, y1, w1, h1, x2, y2, w2, h2):
        """Return True if two rectangles touch or overlap."""
        return not (
            x1 + w1 <= x2 or
            x1 >= x2 + w2 or
            y1 + h1 <= y2 or
            y1 >= y2 + h2
        )

    def check_if_frog_hit_car(self):
        """Check if the frog touched any car."""
        for car in self.cars:
            if self.rectangles_overlap(
                self.frog_x, self.frog_y, FROG_SIZE, FROG_SIZE,
                car["x"], car["y"], car["width"], car["height"]
            ):
                self.is_game_over = True
                return

    def check_if_frog_on_log(self):
        """
        Check if the frog is standing on a log.
        If yes, move the frog with the log.
        If not, the frog falls in the water.
        """
        frog_is_on_log = False

        for log in self.logs:
            if self.rectangles_overlap(
                self.frog_x, self.frog_y, FROG_SIZE, FROG_SIZE,
                log["x"], log["y"], log["width"], log["height"]
            ):
                frog_is_on_log = True
                self.frog_x += log["speed"]
                break

        if not frog_is_on_log:
            self.is_game_over = True
            return

        # If the frog rides a log off the screen, lose the game
        if self.frog_x < 0 or self.frog_x + FROG_SIZE > WINDOW_WIDTH:
            self.is_game_over = True

    def check_collisions(self):
        """Check win condition and danger conditions."""
        frog_row = self.frog_y // CELL_SIZE

        # Win if frog reaches the top row
        if frog_row == GOAL_ROW:
            self.has_won = True
            return

        # Road rows: frog must avoid cars
        if frog_row in ROAD_ROWS:
            self.check_if_frog_hit_car()

        # Water rows: frog must stay on a log
        if frog_row in WATER_ROWS:
            self.check_if_frog_on_log()

    def draw_cars(self):
        """Draw all cars."""
        for car in self.cars:
            self.canvas.create_rectangle(
                car["x"],
                car["y"],
                car["x"] + car["width"],
                car["y"] + car["height"],
                fill=COLOR_CAR,
                outline=COLOR_BLACK
            )

    def draw_logs(self):
        """Draw all logs."""
        for log in self.logs:
            self.canvas.create_rectangle(
                log["x"],
                log["y"],
                log["x"] + log["width"],
                log["y"] + log["height"],
                fill=COLOR_LOG,
                outline=COLOR_BLACK
            )

    def draw_frog(self):
        """Draw the frog."""
        self.canvas.create_rectangle(
            self.frog_x,
            self.frog_y,
            self.frog_x + FROG_SIZE,
            self.frog_y + FROG_SIZE,
            fill=COLOR_FROG,
            outline=COLOR_BLACK
        )

    def draw_all_objects(self):
        """Draw cars, logs, and frog."""
        self.draw_cars()
        self.draw_logs()
        self.draw_frog()

    def draw_message(self, text, color):
        """Show a message in the middle of the screen."""
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            text=text,
            fill=color,
            font=("Arial", 24, "bold")
        )

    def update_game(self):
        """Main game loop."""
        self.canvas.delete("all")
        self.draw_background_rows()

        if not self.is_game_over and not self.has_won:
            self.move_all_objects()
            self.check_collisions()

        self.draw_all_objects()

        if self.is_game_over:
            self.draw_message("Game Over! Press R to restart", COLOR_CAR)
        elif self.has_won:
            self.draw_message("You Win! Press R to restart", COLOR_BLACK)

        self.root.after(GAME_SPEED_MS, self.update_game)


# -----------------------------
# START THE GAME
# -----------------------------
root = tk.Tk()
game = FroggerGame(root)
root.mainloop()