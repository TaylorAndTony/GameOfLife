import random
from pprint import pp
import os
import time


class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = [[0 for _ in range(self.width)]
                       for _ in range(self.height)]

    def manual_set_map(self, target_map: list):
        """ 手动设定当前帧，一个只有 1 和 0 的二维列表 """
        if len(target_map) != self.height:
            raise ValueError('手动设定的高度与创建的高度不符')
        if len(target_map[0]) != self.width:
            raise ValueError('手动设定的宽度与创建的高度不符')
        self.screen = target_map

    def random_init(self, is_alive=0.3):
        """ 随机化地图，使用 is_alive 控制活细胞概率 """
        for line in range(self.height):
            for pix in range(self.width):
                if random.uniform(0, 1) < is_alive:
                    self.screen[line][pix] = 1

    def __get_cell(self, i, j) -> int:
        """ 返回 i， j 细胞状态 """
        i = i % self.height
        j = j % self.width
        return self.screen[i][j]

    def __get_nearby_count(self, i, j) -> int:
        """ 返回第 i 行第 j 个细胞周围的活细胞数量 """
        nearby = []
        # i: 行
        # j: 列
        # 左上，上，右上，右，右下，下，左下，左
        nearby.append(self.__get_cell(i - 1, j - 1))
        nearby.append(self.__get_cell(i - 1, j))
        nearby.append(self.__get_cell(i - 1, j + 1))
        nearby.append(self.__get_cell(i, j + 1))
        nearby.append(self.__get_cell(i + 1, j + 1))
        nearby.append(self.__get_cell(i + 1, j))
        nearby.append(self.__get_cell(i + 1, j - 1))
        nearby.append(self.__get_cell(i, j - 1))
        # 统计 nearby 中 1 的个数即可
        is_alive = [i for i in nearby if i == 1]
        return len(is_alive)

    def next_frame(self) -> None:
        """ 推演下一帧 """
        new_screen = [[0 for _ in range(self.width)]
                      for _ in range(self.height)]
        # 遍历屏幕上的每一个细胞
        for i in range(self.height):
            for j in range(self.width):
                count = self.__get_nearby_count(i, j)
                # alive
                if count == 3:
                    new_screen[i][j] = 1
                # dead
                elif count < 2 or count > 3:
                    new_screen[i][j] = 0
                # stay
                else:
                    new_screen[i][j] = self.screen[i][j]
        # 更新
        self.screen = new_screen

    def immediate_check_screen(self, on='██', off='  ') -> None:
        """ 立即查看当前地图 """
        for line in self.screen:
            for pix in line:
                # 用 char 替代活细胞
                # ■□
                char = on if pix else off
                print(char, end='')
            print()

    def update_and_check(self, sleep=None) -> None:
        """ 更新并打印当前帧 """
        self.next_frame()
        self.immediate_check_screen()
        if sleep:
            time.sleep(sleep)

    def update_generations(self, gen, delay=1):
        """ 推演 gen 代 """
        for i in range(gen):
            os.system('cls')
            print('generation {}/{}'.format(i+1, gen))
            self.update_and_check(delay)


if __name__ == '__main__':
    game = GameOfLife(8, 8)
    game.manual_set_map([
        [0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ])
    game.update_generations(50, 0.1)
