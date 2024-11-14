from window import Window
from maze import Point, Line, Cell, Maze

def main():
    win = Window(800, 600)

    maze = Maze(100, 100, 5, 5, 50, 50, win, seed=666)
    maze.solve()

    win.wait_for_close()

if __name__ == "__main__":
    main()
