import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master, main_menu_callback):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x400")

        self.paused = False
        self.main_menu_callback = main_menu_callback

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"

        self.food = self.spawn_food()

        self.score = 0
        self.score_label = self.canvas.create_text(50, 10, text="Score: 0", fill="yellow", font=("Helvetica", 12), anchor="nw")

        self.master.bind("<Key>", self.handle_keypress)

        self.update()

    def spawn_food(self):
        x = random.randint(3, 37) * 10
        y = random.randint(3, 37) * 10
        return self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="red")

    def handle_keypress(self, event):
        key = event.keysym
        if key == "Up" and not self.direction == "Down" or \
                key == "Down" and not self.direction == "Up" or \
                key == "Left" and not self.direction == "Right" or \
                key == "Right" and not self.direction == "Left":
            self.direction = key
        elif key == "p":
            self.toggle_pause()
        elif key == "r":
            self.redirect_to_main_menu()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.canvas.create_text(200, 200, text="Paused", fill="white", font=("Helvetica", 16), tags="pause")
        else:
            self.canvas.delete("pause")
            self.update()

    def reset_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.food = self.spawn_food()
        self.score = 0
        self.update_score()
        self.paused = False
        self.canvas.delete("pause", "game_over")
        self.update()

    def redirect_to_main_menu(self):
        self.master.destroy()
        self.main_menu_callback()

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Up":
            new_head = (head[0], head[1] - 10)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 10)
        elif self.direction == "Left":
            new_head = (head[0] - 10, head[1])
        elif self.direction == "Right":
            new_head = (head[0] + 10, head[1])

        self.snake = [new_head] + self.snake[:-1]

    def check_collision(self):
        head = self.snake[0]
        if head in self.snake[1:]:
            return True
        if (head[0] < 0 or head[0] >= 400 or
                head[1] < 0 or head[1] >= 400):
            return True
        return False

    def check_food(self):
        head = self.snake[0]
        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))
            self.canvas.delete(self.food)
            self.food = self.spawn_food()
            self.score += 10
            self.update_score()

    def update_score(self):
        self.canvas.itemconfig(self.score_label, text="Score: {}".format(self.score))

    def update(self):
        if not self.paused and not self.check_collision():
            self.move_snake()
            self.check_food()
            self.draw_snake()
            self.master.after(100, self.update)
        elif self.check_collision():
            self.canvas.create_text(200, 200, text="Game Over! Score: {}. \n    Press 'r' to retry.".format(self.score),
                                    fill="white", font=("Helvetica", 16), tags="game_over")
        else:
            self.canvas.create_text(200, 200, text="Paused", fill="white", font=("Helvetica", 16), tags="pause")

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green",
                                         tags="snake")


class SnakeMainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game Main Menu")
        self.master.geometry("400x400")

        self.background_label = tk.Label(self.master, bg="black")
        self.background_label.place(relwidth=1, relheight=1)

        self.title_label = tk.Label(self.master, text="Snake Game", font=("Helvetica", 24), bg="black", fg="white")
        self.title_label.pack(pady=20)

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.destroy)
        self.quit_button.pack(pady=10)

    def start_game(self):
        self.master.destroy()
        root = tk.Tk()
        game = SnakeGame(root, self.redirect_to_main_menu)
        root.mainloop()

    def redirect_to_main_menu(self):
        self.master = tk.Tk()
        main_menu = SnakeMainMenu(self.master)
        self.master.mainloop()


if __name__ == "__main__":
    main_menu_root = tk.Tk()
    main_menu = SnakeMainMenu(main_menu_root)
    main_menu_root.mainloop()
