import tkinter as tk
import random

WIDTH = 800
HEIGHT = 400
BAR_WIDTH = 8
DELAY = 10  # milliseconds (smaller = faster)

class AlgoVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Sorting Algorithm Visualizer")

        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg='white')
        self.canvas.pack()

        self.data = [random.randint(10, HEIGHT) for _ in range(WIDTH // BAR_WIDTH)]
        self.draw_bars(self.data)

        self.i = 0
        self.j = 0

        start_button = tk.Button(master, text="Start Bubble Sort", command=self.bubble_sort_step)
        start_button.pack(pady=10)

    def draw_bars(self, data, color_array=None):
        self.canvas.delete("all")
        if color_array is None:
            color_array = ["blue"] * len(data)

        for i, val in enumerate(data):
            x0 = i * BAR_WIDTH
            y0 = HEIGHT - val
            x1 = (i + 1) * BAR_WIDTH
            y1 = HEIGHT
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
        
        self.master.update_idletasks()

    def bubble_sort_step(self):
        if self.i < len(self.data):
            if self.j < len(self.data) - self.i - 1:
                color_array = ["blue"] * len(self.data)
                color_array[self.j] = "red"
                color_array[self.j + 1] = "red"

                if self.data[self.j] > self.data[self.j + 1]:
                    self.data[self.j], self.data[self.j + 1] = self.data[self.j + 1], self.data[self.j]
                
                self.j += 1
                self.draw_bars(self.data, color_array)
                self.master.after(DELAY, self.bubble_sort_step)
            else:
                self.j = 0
                self.i += 1
                self.master.after(DELAY, self.bubble_sort_step)
        else:
            self.draw_bars(self.data, ["green"] * len(self.data))

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    visualizer = AlgoVisualizer(root)
    root.mainloop()
