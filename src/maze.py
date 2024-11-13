import time

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

    def draw(self):
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "black")

    def draw_move(self, to_cell, undo = False):
        if undo:
            self._win.draw_line(Line(self.get_center(), to_cell.get_center()), "gray")
        else:
            self._win.draw_line(Line(self.get_center(), to_cell.get_center()), "red")

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
            win
        ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()

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

