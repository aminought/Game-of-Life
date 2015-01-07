from tkinter import *
from tkinter import ttk
import copy


class Application:
    master = None
    canvas = None
    hor_cells = 250
    ver_cells = 100
    cell_width = 5
    width = hor_cells*(cell_width+1)+1
    height = ver_cells*(cell_width+1)+1
    is_loop = False
    cells = []

    def __init__(self, master):
        self.master = master
        self.create_canvas()
        self.draw_grid()
        self.clear_cells()
        self.create_widgets()

    def create_canvas(self):
        self.canvas = Canvas(self.master, width=self.width, height=self.height, bg="white")
        self.canvas.grid(row=1, column=1, columnspan=7)
        self.canvas.bind('<B1-Motion>', self.add_dot)
        self.canvas.bind('<Button-1>', self.add_dot)
        self.canvas.bind('<B3-Motion>', self.remove_dot)
        self.canvas.bind('<Button-3>', self.remove_dot)

    def draw_grid(self):
        for i in range(1, self.width, 1+self.cell_width):
            self.canvas.create_line(i, 0, i, self.height, fill="grey")
        for j in range(1, self.height, 1+self.cell_width):
            self.canvas.create_line(0, j, self.width, j, fill="grey")

    def create_widgets(self):
        start_button = ttk.Button(self.master, text="Start", command=self.on_start)
        start_button.grid(row=2, column=3)
        stop_button = ttk.Button(self.master, text="Stop", command=self.on_stop)
        stop_button.grid(row=2, column=4)
        clear_button = ttk.Button(self.master, text="Clear", command=self.on_clear)
        clear_button.grid(row=2, column=5)

    def on_start(self):
        self.is_loop = True
        self.start_loop()

    def start_loop(self):
        if self.is_loop:
            self.loop()
            self.master.after(100, self.start_loop)

    def on_stop(self):
        self.is_loop = False

    def on_clear(self):
        self.clear_cells()
        self.canvas.delete(ALL)
        self.draw_grid()

    def loop(self):
        tmp = copy.deepcopy(self.cells)
        for h, hor in enumerate(tmp):
            for v, cell in enumerate(hor):
                alive = 0
                if h-1 >= 0:
                    if v-1 >= 0:
                        if tmp[h-1][v-1] == 1:
                            alive += 1
                    if v+1 < len(hor):
                        if tmp[h-1][v+1] == 1:
                            alive += 1
                    if tmp[h-1][v] == 1:
                        alive += 1
                if h+1 < len(tmp):
                    if v-1 >= 0:
                        if tmp[h+1][v-1] == 1:
                            alive += 1
                    if v+1 < len(hor):
                        if tmp[h+1][v+1] == 1:
                            alive += 1
                    if tmp[h+1][v] == 1:
                        alive += 1
                if v-1 >= 0:
                    if tmp[h][v-1] == 1:
                        alive += 1
                if v+1 < len(hor):
                    if tmp[h][v+1] == 1:
                        alive += 1

                if cell == 0 and alive == 3:
                    self.cells[h][v] = 1
                elif cell == 1:
                    if alive < 2 or alive > 3:
                        self.cells[h][v] = 0
        self.draw_life()

    def clear_cells(self):
        self.cells = [[0 for x in range(self.hor_cells)] for x in range(self.ver_cells)]

    def add_dot(self, event):
        x = event.x
        y = event.y
        self.cells[y//(1+self.cell_width)][x//(1+self.cell_width)] = 1
        self.draw_life()

    def remove_dot(self, event):
        x = event.x
        y = event.y
        self.cells[y//(1+self.cell_width)][x//(1+self.cell_width)] = 0
        self.draw_life()

    def draw_life(self):
        self.canvas.delete(ALL)
        self.draw_grid()
        for h, hor in enumerate(self.cells):
            for v, cell in enumerate(hor):
                if cell == 1:
                    self.canvas.create_rectangle(v*(self.cell_width+1)+2,
                                                 h*(self.cell_width+1)+2,
                                                 (1+v)*(self.cell_width+1),
                                                 (1+h)*(self.cell_width+1),
                                                 fill="black", outline="black")

root = Tk()
app = Application(root)
root.mainloop()