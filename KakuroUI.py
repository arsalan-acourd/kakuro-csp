import math
import random
import sys
from time import time
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, RIGHT
from BackTrackSolver import BackTrackSolver
from KakuroRandomGame import KakuroRandomGame

MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9
root = None


class KakuroError(Exception):
    pass


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func


def load_another():
    global root
    if root:
        root.destroy()
    game = KakuroRandomGame()
    root = Tk()
    ui = KakuroUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()


def load_for_100_time():
    global root
    t = time()
    print("time to load", t)
    for i in range(100):
        if root:
            root.destroy()
        game = KakuroRandomGame()
        root = Tk()
        ui = KakuroUI(root, game)
        root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
        ui.solve()
    print("average time on 100 try :", (time() - t) / 100)

class KakuroUI(Frame):
    def __init__(self, parent, game):
        self.canvas = None
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent
        self.row, self.col = -1, -1
        self.back_track_solver = BackTrackSolver(game.data_table)
        self.initUI()

    def initUI(self):
        if self.game.gameId != 0:
            self.parent.title("Kakuro | Puzzle: " + str(self.game.gameId))
        else:
            self.parent.title("Kakuro | Puzzle: Custom")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill=BOTH, side=TOP)

        solve_button = Button(self, text="Solve!", command=self.solve)
        solve_button.pack(side=RIGHT, padx=10)
        clear_button = Button(self, text="Clear answers", command=self.clear_answers)
        clear_button.pack(side=RIGHT)
        try_button = Button(self, text="Try another", command=load_another)
        try_button.pack(side=RIGHT, padx=10)

        self.draw_grid()
        self.draw_puzzle()

    def draw_grid(self):
        for i in range(10):
            stretch = 0
            if i % 9 == 0:
                stretch = 1
            self.canvas.create_line(
                MARGIN + i * SIDE, MARGIN - stretch,
                MARGIN + i * SIDE, HEIGHT - MARGIN + stretch,
                width=2
            )

            self.canvas.create_line(
                MARGIN, MARGIN + i * SIDE,
                        WIDTH - MARGIN, MARGIN + i * SIDE,
                width=2
            )

        for i in range(9):
            for j in range(9):
                if [i, j] not in self.game.data_fills:
                    self.canvas.create_rectangle(MARGIN + j * SIDE + 1, MARGIN + i * SIDE + 1,
                                                 MARGIN + j * SIDE + SIDE - 2, MARGIN + i * SIDE + SIDE - 2,
                                                 outline="gray", fill="gray", tag="grays")
                    self.canvas.create_line(
                        MARGIN + j * SIDE, MARGIN + i * SIDE,
                        MARGIN + j * SIDE + SIDE, MARGIN + i * SIDE + SIDE,
                        width=2, tag="grayliners"
                    )

    def draw_puzzle(self):
        self.canvas.delete("numbersfilled")
        for elem in self.game.data_totals:
            i = elem[2]
            j = elem[3]
            if elem[1] == 'v':
                modif = -1
            else:
                modif = 1
            self.canvas.create_text(
                MARGIN + j * SIDE + SIDE / 2 + modif * SIDE / 4,
                MARGIN + i * SIDE + SIDE / 2 + (-modif) * SIDE / 4,
                text=elem[0], tags="numbers",
                fill="black"
            )
        for elem in self.game.data_filled:
            i = elem[0]
            j = elem[1]
            self.canvas.create_text(
                MARGIN + j * SIDE + SIDE / 2,
                MARGIN + i * SIDE + SIDE / 2,
                font=("Purissa", 20),
                text=elem[2], tags="numbersfilled",
                fill="slate gray"
            )

    def draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            self.canvas.create_rectangle(
                MARGIN + math.floor(self.col) * SIDE + 1,
                MARGIN + math.floor(self.row) * SIDE + 1,
                MARGIN + (math.floor(self.col) + 1) * SIDE - 1,
                MARGIN + (math.floor(self.row) + 1) * SIDE - 1,
                outline="red", tags="cursor"
            )

    def create_circs(self, addrs):
        if len(addrs) == 0:
            return
        for elem in addrs:
            self.canvas.create_oval(
                # Figure out the inversion!
                MARGIN + SIDE * elem[1], MARGIN + SIDE * elem[0],
                MARGIN + SIDE * elem[1] + SIDE, MARGIN + SIDE * elem[0] + SIDE,
                tags="circ", outline="red", width=2.0
            )

    def draw_victory(self):
        self.canvas.create_oval(
            MARGIN - 10, MARGIN - 10,
            MARGIN + 50, MARGIN + 50,
            tags="victory", fill="dark orange", outline="orange"
        )
        self.canvas.create_text(
            MARGIN + 22,
            MARGIN + 22,
            text="Correct!", tags="victory",
            fill="white", font=("Ubuntu", 11)
        )

    def road(self, addr):
        if bool(addr[0] == self.row) == bool(addr[1] == self.col):
            return False
        elif addr[0] == self.row:
            curr_row = self.row
            for iter in range(min(addr[1], self.col), max(addr[1], self.col)):
                if [curr_row, iter] not in self.game.data_fills:
                    return False
            return True
        else:
            curr_col = self.col
            for iter in range(min(addr[0], self.row), max(addr[0], self.row)):
                if [iter, curr_col] not in self.game.data_fills:
                    return False
            return True

    def clear_answers(self):
        self.game.data_filled = []
        self.canvas.delete("victory")
        self.canvas.delete("circ")
        self.draw_puzzle()

    def set_value(self, row, col, value):
        self.canvas.delete("victory")
        self.canvas.delete("circ")
        if self.game.game_over:
            return
        self.game.data_table[row][col] = value
        if [row, col] in self.game.data_fills:
            found_flag = False
            for ind, item in enumerate(self.game.data_filled):
                if item[0] == row and item[1] == col:
                    found_flag = True
                    self.game.data_filled[ind][2] = value
            if not found_flag:
                self.game.data_filled = self.game.data_filled + [[row, col, value]]

            circlists = []
            for elem in self.game.data_filled:
                if self.road(elem) and elem[2] == value:
                    if [row, col] not in circlists:
                        circlists = circlists + [[row, col]]
                    if [elem[0], elem[1]] not in circlists:
                        circlists = circlists + [[elem[0], elem[1]]]
            self.create_circs(circlists)
            self.draw_cursor()
            self.draw_puzzle()
            if self.game.check_win():
               self.draw_victory()

    @timer_func
    def solve(self):
        self.game.data_filled = []
        self.canvas.delete("victory")
        self.canvas.delete("circ")
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # Remember to zero down the indices

        for [i, j] in self.game.data_fills:
            self.back_track_solver.add_variable([i, j], options)

        constraint_num = 0
        variable_constrain_number = {}
        for [total_sum, row_or_col, i, j] in self.game.data_totals:
            var_list = []
            if row_or_col == 'v':
                for i1 in range(i + 1, 9):
                    if self.game.data_table[i1][j] == 'x':
                        break
                    if (i1, j) in variable_constrain_number:
                        variable_constrain_number[(i1, j)].append(constraint_num)
                    else:
                        variable_constrain_number[(i1, j)] = [constraint_num]
                    var_list.append([i1, j])
            else:
                for j1 in range(j + 1, 9):
                    if self.game.data_table[i][j1] == 'x':
                        break
                    if (i, j1) in variable_constrain_number:
                        variable_constrain_number[(i, j1)].append(constraint_num)
                    else:
                        variable_constrain_number[(i, j1)] = [constraint_num]
                    var_list.append([i, j1])
            self.back_track_solver.add_constraint([var_list, total_sum])
            constraint_num += 1

        self.back_track_solver.var_constraint = variable_constrain_number
        solutions = self.back_track_solver.solve()[0]
        # print("solution number : \n", solutions)
        for var in solutions:
            self.set_value(var[0], var[1], solutions[var])