from window import Window
from point import Point, Line, Cell

def main():
    win = Window(800, 600)

    cell1 = Cell(Point(100, 100), Point(150, 150), win)
    cell1.draw()

    cell2 = Cell(Point(200, 200), Point(250, 250), win)
    cell2.has_left_wall = False
    cell2.draw()

    cell3 = Cell(Point(300, 300), Point(350, 350), win)
    cell3.has_right_wall = False
    cell3.draw()

    cell4 = Cell(Point(400, 400), Point(450, 450), win)
    cell4.has_top_wall = False
    cell4.draw()

    cell5 = Cell(Point(500, 500), Point(550, 550), win)
    cell5.has_bottom_wall = False
    cell5.draw()

    win.wait_for_close()

if __name__ == "__main__":
    main()
