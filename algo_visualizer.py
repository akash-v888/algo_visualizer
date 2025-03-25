import tkinter as tk
import random

WIDTH = 1000
HEIGHT = 400
BAR_WIDTH = 12

class AlgoVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Sorting Algorithm Visualizer")

        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg='white')
        self.canvas.pack()

        self.num_bars = 80
        self.data = [random.randint(10, HEIGHT) for _ in range(self.num_bars)]
        self.draw_bars(self.data)

        self.i = 0
        self.j = 0
        self.sorting = False

        controls_frame = tk.Frame(master)
        controls_frame.pack(pady=10)

        # Dropdown menu
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("Bubble Sort")
        algo_menu = tk.OptionMenu(controls_frame, self.algorithm_var, "Bubble Sort", "Insertion Sort", "Selection Sort")
        algo_menu.pack(side=tk.LEFT, padx=10)

        self.delay_slider = tk.Scale(controls_frame, from_=1, to=200, label="Speed (ms)", orient=tk.HORIZONTAL)
        self.delay_slider.set(20)
        self.delay_slider.pack(side=tk.LEFT, padx=10)

        start_button = tk.Button(controls_frame, text="Start", command=self.start_sorting)
        start_button.pack(side=tk.LEFT, padx=10)

        reset_button = tk.Button(controls_frame, text="Reset", command=self.reset)
        reset_button.pack(side=tk.LEFT, padx=10)

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

    def reset(self):
        self.data = [random.randint(10, HEIGHT) for _ in range(self.num_bars)]
        self.i = 0
        self.j = 0
        self.sorting = False
        self.draw_bars(self.data)

    def start_sorting(self):
        algo = self.algorithm_var.get()
        self.i = 0
        self.j = 0
        self.sorting = True

        if algo == "Bubble Sort":
            self.bubble_sort_step()
        elif algo == "Insertion Sort":
            self.insertion_sort_step()
        elif algo == "Selection Sort":
            self.selection_sort_step()

    # --------------------
    # Sorting Algorithms
    # --------------------

    def bubble_sort_step(self):
        if self.i < len(self.data):
            if self.j < len(self.data) - self.i - 1:
                colors = ["blue"] * len(self.data)
                colors[self.j] = "red"
                colors[self.j + 1] = "red"

                if self.data[self.j] > self.data[self.j + 1]:
                    self.data[self.j], self.data[self.j + 1] = self.data[self.j + 1], self.data[self.j]

                self.j += 1
                self.draw_bars(self.data, colors)
                self.master.after(self.delay_slider.get(), self.bubble_sort_step)
            else:
                self.j = 0
                self.i += 1
                self.master.after(self.delay_slider.get(), self.bubble_sort_step)
        else:
            self.draw_bars(self.data, ["green"] * len(self.data))

    def insertion_sort_step(self):
        if self.i < len(self.data):
            key = self.data[self.i]
            j = self.i - 1
            while j >= 0 and self.data[j] > key:
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key

            colors = ["green" if x <= self.i else "blue" for x in range(len(self.data))]
            colors[self.i] = "red"
            self.draw_bars(self.data, colors)

            self.i += 1
            self.master.after(self.delay_slider.get(), self.insertion_sort_step)
        else:
            self.draw_bars(self.data, ["green"] * len(self.data))

    def selection_sort_step(self):
        if self.i < len(self.data):
            min_idx = self.i
            for j in range(self.i + 1, len(self.data)):
                if self.data[j] < self.data[min_idx]:
                    min_idx = j
            self.data[self.i], self.data[min_idx] = self.data[min_idx], self.data[self.i]

            colors = ["green" if x <= self.i else "blue" for x in range(len(self.data))]
            colors[self.i] = "red"
            self.draw_bars(self.data, colors)

            self.i += 1
            self.master.after(self.delay_slider.get(), self.selection_sort_step)
        else:
            self.draw_bars(self.data, ["green"] * len(self.data))

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    visualizer = AlgoVisualizer(root)
    root.mainloop()
