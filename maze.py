# 迷宫基本规则
# 砸墙理解方法：每一个格子理解为一个房间，有四堵墙
# 1. 当隔壁房间没有去过才可以砸墙
# 2. 去到终点后，执行 3
# 3. 当有房间没有去过，在其最近已经去过的房间随机选一个，按照规则 1 开始砸墙，直到不可以砸墙，重复，直到不存在没有去过的房间
import tkinter as tk
import random
import time

HEIGHT = 4
WIDTH = 6

MAZE_IN = [1, 1]
MAZE_OUT = [HEIGHT, WIDTH]

CELL_SIZE = 50
BORDER_SIZE = 20


class GUI:
    def __init__(self, height, width, _maze_):
        self.maze = _maze_
        self.height = height
        self.width = width
        # Windows size
        self.windows_height = self.height * CELL_SIZE + 2 * BORDER_SIZE
        self.windows_width = self.width * CELL_SIZE + 2 * BORDER_SIZE
        # tkinter
        self.root = tk.Tk()
        self.root.title("Maze 27/01-2021 @DioPong")
        self.root.geometry(f"{self.windows_width}x{self.windows_height}+500+200")
        self.cv = tk.Canvas(self.root, bg="white", width=self.windows_width, height=self.windows_height)
        self.maze_initial()
        walls = self.maze_format()
        self.draw_maze(walls=walls)
        self.root.mainloop()

    def maze_initial(self):
        # self.cv.create_rectangle(20, 20, self.windows_width-20, self.windows_height-20)
        # self.cv.pack()
        for x in range(self.width):
            for y in range(self.height):
                cell_x = BORDER_SIZE + x * CELL_SIZE
                cell_y = BORDER_SIZE + y * CELL_SIZE
                self.cv.create_rectangle(cell_x, cell_y, cell_x + CELL_SIZE, cell_y + CELL_SIZE, outline="black")
        self.cv.pack()

    def draw_maze(self, walls=None):
        def revise(num, flag1, flag2):
            # flag1 横竖线标记。flag2 偏移量，标记终点
            return BORDER_SIZE + ((num - flag1) // 2 + flag2) * CELL_SIZE

        for wall in walls:
            # 需要判别画的是横线还是竖线 0-> 竖线 1->横线
            if wall[1] % 2:  # 横线
                self.cv.create_line(revise(wall[1], 1, 0), revise(wall[0], 1, 1),
                                    revise(wall[1], 1, 1), revise(wall[0], 1, 1),
                                    fill="white")
            else:  # 竖线
                self.cv.create_line(revise(wall[1], 0, 0), revise(wall[0], 0, 1),
                                    revise(wall[1], 0, 0), revise(wall[0], 0, 0),
                                    fill="white")
        #
        # # 出入口
        # def door(coordinate):
        #     _doors_ = []
        #     x, y = coordinate[0], coordinate[1]
        #     _doors_.append([x - 1, y]) if x - 1 == 0 else ...
        #     _doors_.append([x + 1, y]) if x + 1 == 2 * self.height else ...
        #     _doors_.append([x, y - 1]) if y - 1 == 0 else ...
        #     _doors_.append([x, y + 1]) if y + 1 == 2 * self.width else ...
        #     return random.choice(_doors_)
        # doors = [door(list(map(lambda x: 2 * x - 1, MAZE_IN)))] + [door(list(map(lambda x: 2 * x - 1, MAZE_OUT)))]
        # print(doors)
        # for gate in doors:
        #     print(gate, gate[0] % 2 == 0)
        #     if gate[0] % 2 == 0:  # 竖线
        #         self.cv.create_line(revise(gate[1], 1, 0), revise(gate[0], 0, 0),
        #                             revise(gate[1], 1, 0), revise(gate[0], 0, 0),
        #                             fill="blue", width=5)
        #     else:  # 横线
        #         self.cv.create_line(revise(gate[1], 0, 1), revise(gate[0], 1, 0),
        #                             revise(gate[1], 0, 1), revise(gate[0], 1, 1),
        #                             fill="red", width=5)

    def maze_format(self):
        path = []
        for x in range(2 * self.width + 1):
            for y in range(2 * self.height + 1):
                if (x + y) % 2 and self.maze[y][x] == 0:
                    path.append([y, x])
        return path


class MAZE:
    def __init__(self, height, width, maze_in, maze_out):
        self.height = height
        self.width = width
        self.maze_in = maze_in
        self.maze_out = maze_out
        self.unvisited = []
        self.visited = []
        self.maze = self.maze_initial()
        self.get_maze_path()

    def maze_initial(self):
        maze_size_width = 2 * self.width + 1
        maze_size_height = 2 * self.height + 1
        _maze_ = [[1 for x in range(maze_size_width)] for y in range(maze_size_height)]
        for column in range(maze_size_height):  # 2
            for cell in range(maze_size_width):  # 3
                if column % 2 and cell % 2:
                    _maze_[column][cell] = 0
                    self.unvisited.append([column, cell])
        return _maze_

    @staticmethod
    def random_choice(next_cell):
        return random.choice(next_cell)

    def get_valid_position(self, coordinate):
        x, y = coordinate[0], coordinate[1]
        valid_next_position = [[x, y - 2], [x + 2, y], [x, y + 2], [x - 2, y]]
        valid_next_position.remove([x + 2, y]) if x == 2 * self.height - 1 or [x + 2, y] not in self.unvisited else ...
        valid_next_position.remove([x, y - 2]) if y == 1 or [x, y - 2] not in self.unvisited else ...
        valid_next_position.remove([x, y + 2]) if y == 2 * self.width - 1 or [x, y + 2] not in self.unvisited else ...
        valid_next_position.remove([x - 2, y]) if x == 1 or [x - 2, y] not in self.unvisited else ...
        return valid_next_position

    def get_maze_path(self):
        maze_in = list(map(lambda x: 2 * x - 1, MAZE_IN))
        maze_out = list(map(lambda x: 2 * x - 1, MAZE_OUT))
        current_cell = maze_in
        self.visited.append(maze_in)
        self.unvisited.remove(maze_in)
        while True:
            if current_cell == maze_out:  # 如果当前单元格是终点，停止；如果存在还没有访问过的房间，继续
                # 当前到达终点，需要重新选
                current_cell = self.random_choice(self.visited)
                continue
            if not self.unvisited:
                break
            valid_next_cells = self.get_valid_position(current_cell)
            # 若当前不可用：
            if not valid_next_cells:
                # 从已选择列表随机选一个，检查其本身附件是否有可用的点，若不满足重复操作，直到找到为止
                current_cell = self.random_choice(self.visited)
                continue
            # 当前可用状态，随机选一个
            next_cell = self.random_choice(valid_next_cells)
            # 开始砸墙
            self.maze[(current_cell[0] + next_cell[0]) // 2][(current_cell[1] + next_cell[1]) // 2] = 0
            # 归并已经扫描，移除未扫描
            self.visited.append(next_cell)
            self.unvisited.remove(next_cell)
            # 跳转到下一个单元格
            current_cell = next_cell


# MAZE类，以数组的形式 返回迷宫
# GUI类将迷宫以图案展示出来

"""
   
    0 1 2 3 4 5 6
   
0   1 1 1 1 1 1 1
1   1 0 1 0 1 0 1
2   1 1 1 1 1 1 1
3   1 0 1 0 1 0 1
4   1 1 1 1 1 1 1

1 1
1 3
-- 1 2
"""

maze = MAZE(HEIGHT, WIDTH, MAZE_IN, MAZE_OUT)
for line in maze.maze:
    print(line)
GUI(_maze_=maze.maze, height=HEIGHT, width=WIDTH)
