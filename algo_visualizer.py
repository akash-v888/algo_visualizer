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

        # Top-level layout for controls
        controls_frame = tk.Frame(master, pady=10)
        controls_frame.pack()

        # --- Row 1: Algorithm & Order ---
        row1 = tk.Frame(controls_frame)
        row1.pack(pady=5)

        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        algo_menu = tk.OptionMenu(row1, self.algorithm_var, 
                                  "Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort", "Quick Sort")
        algo_menu.config(width=15)
        tk.Label(row1, text="Algorithm:").pack(side=tk.LEFT, padx=5)
        algo_menu.pack(side=tk.LEFT, padx=10)

        self.order_var = tk.StringVar(value="Random")
        order_menu = tk.OptionMenu(row1, self.order_var, "Random", "In Order", "Reverse Order")
        order_menu.config(width=15)
        tk.Label(row1, text="Data Order:").pack(side=tk.LEFT, padx=5)
        order_menu.pack(side=tk.LEFT, padx=10)

        # --- Row 2: Sliders ---
        row2 = tk.Frame(controls_frame)
        row2.pack(pady=5)

        self.size_slider = tk.Scale(row2, from_=10, to=100, label="Number of Bars", orient=tk.HORIZONTAL, length=200)
        self.size_slider.set(self.num_bars)
        self.size_slider.pack(side=tk.LEFT, padx=20)

        self.delay_slider = tk.Scale(row2, from_=1, to=200, label="Speed (ms)", orient=tk.HORIZONTAL, length=200)
        self.delay_slider.set(20)
        self.delay_slider.pack(side=tk.LEFT, padx=20)

        # --- Row 3: Buttons ---
        row3 = tk.Frame(controls_frame)
        row3.pack(pady=10)

        start_button = tk.Button(row3, text="Start", width=12, bg="#4CAF50", fg="black", command=self.start_sorting)
        start_button.pack(side=tk.LEFT, padx=20)

        reset_button = tk.Button(row3, text="Reset", width=12, bg="#f44336", fg="black", command=self.reset)
        reset_button.pack(side=tk.LEFT, padx=20)


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
        self.num_bars = self.size_slider.get()
        order = self.order_var.get()

        if order == "Random":
            self.data = [random.randint(10, HEIGHT) for _ in range(self.num_bars)]
        elif order == "In Order":
            self.data = list(range(10, HEIGHT, (HEIGHT - 10) // self.num_bars))[:self.num_bars]
        elif order == "Reverse Order":
            self.data = list(range(HEIGHT, 10, -((HEIGHT - 10) // self.num_bars)))[:self.num_bars]

        # Recalculate bar width to fit the new number of bars
        global BAR_WIDTH
        BAR_WIDTH = WIDTH // self.num_bars

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
        elif algo == "Merge Sort":
            self.merge_sort_animate()
        elif algo == "Quick Sort":
            self.quick_sort_animate()

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
    

    def merge_sort_animate(self):
        self.actions = []
        self.merge_sort(self.data, 0, len(self.data) - 1)
        self.animate_merge_step(0)

    def merge_sort(self, arr, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(arr, left, mid)
            self.merge_sort(arr, mid + 1, right)
            self.merge(arr, left, mid, right)

    def merge(self, arr, left, mid, right):
        left_copy = arr[left:mid + 1]
        right_copy = arr[mid + 1:right + 1]
        i = j = 0
        k = left

        while i < len(left_copy) and j < len(right_copy):
            if left_copy[i] <= right_copy[j]:
                arr[k] = left_copy[i]
                self.actions.append((arr[:], [k]))
                i += 1
            else:
                arr[k] = right_copy[j]
                self.actions.append((arr[:], [k]))
                j += 1
            k += 1

        while i < len(left_copy):
            arr[k] = left_copy[i]
            self.actions.append((arr[:], [k]))
            i += 1
            k += 1

        while j < len(right_copy):
            arr[k] = right_copy[j]
            self.actions.append((arr[:], [k]))
            j += 1
            k += 1

    def animate_merge_step(self, idx):
        if idx < len(self.actions):
            snapshot, highlights = self.actions[idx]
            color_array = ["green" if i in highlights else "blue" for i in range(len(snapshot))]
            self.data = snapshot
            self.draw_bars(snapshot, color_array)
            self.master.after(self.delay_slider.get(), lambda: self.animate_merge_step(idx + 1))
        else:
            self.draw_bars(self.data, ["green"] * len(self.data))


    def quick_sort_animate(self):
        self.actions = []
        self.quick_sort(self.data, 0, len(self.data) - 1)
        self.animate_quick_step(0)

    def quick_sort(self, arr, low, high):
        if low < high:
            pivot_index = self.partition(arr, low, high)
            self.quick_sort(arr, low, pivot_index - 1)
            self.quick_sort(arr, pivot_index + 1, high)

    def partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.actions.append((arr[:], [i, j]))
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.actions.append((arr[:], [i + 1, high]))
        return i + 1

    def animate_quick_step(self, idx):
        if idx < len(self.actions):
            snapshot, highlights = self.actions[idx]
            color_array = ["blue"] * len(snapshot)
            for i in highlights:
                color_array[i] = "red"
            self.data = snapshot
            self.draw_bars(snapshot, color_array)
            self.master.after(self.delay_slider.get(), lambda: self.animate_quick_step(idx + 1))
        else:
            self.draw_bars(self.data, ["green"] * len(self.data))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sorting Algorithm Visualizer")

    root.option_add("*Font", ("Segoe UI", 10))

    visualizer = AlgoVisualizer(root)
    root.mainloop()
