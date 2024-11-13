from window import Window
from point import Point, Line

def main():
    win = Window(800, 600)
    line = Line(Point(100, 100), Point(100, 200))
    win.draw_line(line, "black")
    line2 = Line(Point(200, 200), Point(300, 200))
    win.draw_line(line2, "red")
    win.wait_for_close()

if __name__ == "__main__":
    main()
