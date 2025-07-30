import tkinter as tk
from PIL import Image, ImageTk
import ctypes
import tkinter.messagebox as mb
import words

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Wordle:
    BG = "#0f172a"
    TEXT_COLOR = "#FFFFFF"
    BTN_COLOR = "#475569"

    def __init__(self):
        self.root = tk.Tk()
        self.width = 600
        self.height = 800
        self.x_co = int(self.root.winfo_screenwidth() / 2) - int(self.width / 2)
        self.y_co = 50
        self.root.geometry(f"{self.width}x{self.height}+{self.x_co}+{self.y_co}")
        self.root.resizable(False, False)
        self.root.configure(background=self.BG)
        self.root.title("Wordle")

        self.guess = ""
        self.current_row = 0
        self.max_rows = 6
        self.word_length = 5
        self.tiles = []
        
        self.tile_images = {
            "empty": ImageTk.PhotoImage(Image.open("images/empty.png").resize((60, 60))),
            "correct": ImageTk.PhotoImage(Image.open("images/correct.png").resize((60, 60))),
            "present": ImageTk.PhotoImage(Image.open("images/present.png").resize((60, 60))),
            "wrong": ImageTk.PhotoImage(Image.open("images/wrong.png").resize((60, 60))),
        }

        self.load_assets()
        self.build_ui()

        self.word_api = words.WordsAPI("words/words.txt")

        # Just For Test - it will show correct answer 
        # print(f"Correct answer: {self.word_api.word}")

        self.root.mainloop()

    def load_assets(self):
        head_img = ImageTk.PhotoImage(Image.open('images/icon.png'))
        self.head_img = head_img  # prevent garbage collection

    def build_ui(self):
        head_label = tk.Label(self.root, image=self.head_img, bd=0, bg=self.BG)
        head_label.pack(pady=10)

        self.grid_frame = tk.Frame(self.root, bg=self.BG)
        self.grid_frame.pack(pady=20)
        self.create_grid()

        self.keyboard_frame = tk.Frame(self.root, bg=self.BG)
        self.keyboard_frame.pack()
        self.create_keyboard()

    def create_grid(self):
        self.tiles.clear()
        for r in range(self.max_rows):
            row_tiles = []
            for c in range(self.word_length):
                tile = tk.Label(self.grid_frame, image=self.tile_images["empty"], text="", compound="center",
                                width=60, height=60, font="Helvetica 20 bold",
                                bg=self.BG, fg="white", bd=0)
                tile.grid(row=r, column=c, padx=5, pady=5)
                tile.image = self.tile_images["empty"]  # keep reference
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

    def create_keyboard(self):
        layout = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for r, keys in enumerate(layout):
            row = tk.Frame(self.keyboard_frame, bg=self.BG)
            row.pack(pady=5)

            if r == 2:
                del_btn = tk.Button(row, text="Del", width=4, height=2, font="Helvetica 10 bold",
                                    command=self.delete_letter, bg=self.BTN_COLOR, fg="white", bd=0)
                del_btn.pack(side="left", padx=2)

            for i, key in enumerate(keys):
                btn = tk.Button(row, text=key, width=4, height=2, font="Helvetica 10 bold",
                                command=lambda k=key: self.add_letter(k),
                                bg=self.BTN_COLOR, fg="white", relief="flat", bd=0)
                btn.pack(side="left", padx=2)

                if r == 2 and key == "M":
                    enter_btn = tk.Button(row, text="Enter", width=5, height=2, font="Helvetica 10 bold",
                                        command=self.check_guess, bg=self.BTN_COLOR, fg="white", bd=0)
                    enter_btn.pack(side="left", padx=2)

    def add_letter(self, char):
        if len(self.guess) < self.word_length:
            self.tiles[self.current_row][len(self.guess)].config(text=char)
            self.guess += char

    def delete_letter(self):
        if self.guess:
            idx = len(self.guess) - 1
            self.tiles[self.current_row][idx].config(text="")
            self.guess = self.guess[:-1]

    def check_guess(self):
        if len(self.guess) != self.word_length:
            return

        guess_upper = self.guess.upper()
        word = self.word_api.word

        status = ["wrong"] * self.word_length
        word_letters = list(word)

        # correct positions
        for i, char in enumerate(guess_upper):
            if word[i] == char:
                status[i] = "correct"
                word_letters[i] = None

        # present letters (wrong position)
        for i, char in enumerate(guess_upper):
            if status[i] == "correct":
                continue
            if char in word_letters:
                status[i] = "present"
                word_letters[word_letters.index(char)] = None

        # update tiles with images and letters
        for i, st in enumerate(status):
            tile = self.tiles[self.current_row][i]
            tile.config(image=self.tile_images[st], text=guess_upper[i], compound="center",
                        fg="white", font="Helvetica 20 bold")
            tile.image = self.tile_images[st]

        if all(s == "correct" for s in status):
            mb.showinfo("You Win!", "🎉 Congratulations! You guessed the word!")
            self.reset()
            return

        self.guess = ""
        self.current_row += 1

        if self.current_row >= self.max_rows:
            mb.showinfo("Game Over", f"The word was:\n{self.word_api.word}")
            self.reset()

    def reset(self):
        self.guess = ""
        self.current_row = 0
        self.word_api = words.WordsAPI("words/words.txt")
        for row in self.tiles:
            for tile in row:
                tile.config(text="", image=self.tile_images["empty"], compound="center",
                            fg="white", font="Helvetica 20 bold")
                tile.image = self.tile_images["empty"]

if __name__ == "__main__":
    Wordle()
