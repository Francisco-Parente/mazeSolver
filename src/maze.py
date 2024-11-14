import time
import random

from tkinter import Canvas

class Point():

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y
        canvas.create_line(x1, y1, x2, y2, fill = fill_color, width = 2)

class Cell():
    
    def __init__(self, point1, point2, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = point1.x
        self._y1 = point1.y
        self._x2 = point2.x
        self._y2 = point2.y
        self._win = window
        self.visited = False

    def draw(self):
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "#d9d9d9")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "#d9d9d9")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "#d9d9d9")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "#d9d9d9")

    def draw_move(self, to_cell, undo = False):
        if undo:
            self._win.draw_line(Line(self._get_center(), to_cell._get_center()), "gray")
        else:
            self._win.draw_line(Line(self._get_center(), to_cell._get_center()), "red")

    def _get_center(self):
        return Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)

class Maze():

    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
            seed = None
        ):
        if seed is not None:
            random.seed(seed)
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            collumn = []
            for j in range(self.num_rows):
                cell = Cell(
                    Point(self.x1 + j * self.cell_size_x, self.y1 + i * self.cell_size_y), 
                    Point(self.x1 + (j + 1) * self.cell_size_x, self.y1 + (i + 1) * self.cell_size_y),
                    self.win
                )
                collumn.append(cell)
            self._cells.append(collumn)
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(-1, -1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            if i > 0:
                to_visit.append((i-1, j))
            if j > 0:
                to_visit.append((i, j-1))
            if i < self.num_cols - 1:
                to_visit.append((i+1, j))
            if j < self.num_rows - 1:
                to_visit.append((i, j +1))
            possible_directions = []
            for cell in to_visit:
                if not self._cells[cell[0]][cell[1]].visited:
                    possible_directions.append(cell)
            if len(possible_directions) == 0:
                return
            else:
                cell = possible_directions[random.randint(0, len(possible_directions) - 1 )]
                if cell[0] == i and cell[1] < j:
                    self._cells[i][j].has_left_wall = False
                    self._cells[i][j-1].has_right_wall = False
                    self._cells[i][j].draw()
                    self._cells[i][j-1].draw()
                    self._break_walls_r(i, j - 1)
                elif cell[0] == i and cell[1] > j:
                    self._cells[i][j].has_right_wall = False
                    self._cells[i][j+1].has_left_wall = False
                    self._cells[i][j].draw()
                    self._cells[i][j+1].draw()
                    self._break_walls_r(i, j+1)
                elif cell[0] < i and cell[1] == j:
                    self._cells[i][j].has_top_wall = False
                    self._cells[i-1][j].has_bottom_wall = False
                    self._cells[i][j].draw()
                    self._cells[i-1][j].draw()
                    self._break_walls_r(i-1, j)
                elif cell[0] > i and cell[1] == j:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[i+1][j].has_top_wall = False
                    self._cells[i][j].draw()
                    self._cells[i+1][j].draw()
                    self._break_walls_r(i+1, j)
                else:
                    raise Exception("check logic for finding neighbours")

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i,j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_cols -1 and j == self.num_rows -1:
            print("Hello")
            return True
        to_visit = []
        if i > 0:
            to_visit.append((i-1, j))
        if j > 0:
            to_visit.append((i, j-1))
        if i < self.num_cols - 1:
            to_visit.append((i+1, j))
        if j < self.num_rows - 1:
            to_visit.append((i, j +1))
        for cell in to_visit:
            if self._cells[cell[0]][cell[1]].visited:
                continue
            if cell[0] == i and cell[1] < j:
                if self._cells[i][j].has_left_wall:
                    continue
                self._cells[i][j].draw_move(self._cells[i][j-1])
                result = self._solve_r(i, j-1)
                if result:
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i][j-1], undo = True)
            elif cell[0] == i and cell[1] > j:
                if self._cells[i][j].has_right_wall:
                    continue
                self._cells[i][j].draw_move(self._cells[i][j+1])
                result = self._solve_r(i, j+1)
                if result:
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i][j+1], undo = True)
            elif cell[0] < i and cell[1] == j:
                if self._cells[i][j].has_top_wall:
                    continue
                self._cells[i][j].draw_move(self._cells[i-1][j])
                result = self._solve_r(i-1, j)
                if result:
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i-1][j], undo = True)
            elif cell[0] > i and cell[1] == j:
                if self._cells[i][j].has_bottom_wall:
                    continue
                self._cells[i][j].draw_move(self._cells[i+1][j])
                result = self._solve_r(i+1, j)
                if result:
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i+1][j], undo = True)

        return False
