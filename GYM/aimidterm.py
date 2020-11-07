import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy.random import seed
from numpy.random import randint
import pygame
import time


# 不限程式語言實作人工生命(Artificial life)，主題與方法不限。
# 以下以健身房的生活方式：
# 空間大小: 100*100 平方
# 初始人比例於空間中: 正常男生0.2，正常女生0.2，泡芙男/女孩0.05, 教練0.05，空位0.5
# 設定空間中角色位置: 隨機
# 設定人每次的移動步數: 1步上下隨機
# 規則1: 教練會將泡芙變成正常
# 規則2: 男生可感測到周遭的味道，並往該方向搜尋女生走過的地方釋放費洛蒙，吸引男生靠近，教練不影響
# 規則3: 一男一女回家，便能夠增加人數量，隨機產生男女
# 規則4: 男/女須在限制的步數或時間內找到男/女，否則死亡

# 設定Time interval
# time.sleep(1)

# Initial

# this function is for changing the exist dots

# move -> update Person statement

class Person:
    def __init__(self, x, y, figure):
        self.x = x
        self.y = y
        self.figure = figure

        self.white = (255, 255, 255)  # grid background
        self.black = (0, 0, 0)  # personal trainer
        self.pink = (255, 105, 180)  # fat woman
        self.purple = (102, 0, 102)  # fat man
        self.blue = (0, 0, 255)  # man
        self.red = (255, 0, 0)  # woman
        self.green = (0, 255, 0)  # personal trainer

        self.colorUpdate()

    def colorUpdate(self):
        if self.figure == 0:
            self.color = self.white
        elif self.figure == 1:
            self.color = self.blue
        elif self.figure == 2:
            self.color = self.red
        elif self.figure == 3:
            self.color = self.green
        elif self.figure == 4:
            self.color = self.pink
        elif self.figure == 5:
            self.color = self.purple


class Gym:
    def __init__(self, windowHeight, windowWidth, blockSize):
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth
        self.blockSize = blockSize
        self.layout = np.zeros((windowHeight, windowWidth),
                               int)  # val (1, 2, 3, 4, 5) means (man, woman, coach, fat_girl, fat_boy)

        '''color set'''
        self.white = (255, 255, 255)  # grid background
        self.black = (0, 0, 0)  # personal trainer
        '''initialize gym layout'''
        self.manRatio = 0.1
        self.womanRatio = 0.1
        self.fatManRatio = 0.025
        self.fatWomanRatio = 0.025
        self.trainerRatio = 0.05
        self.gymSpaceRatio = 0.7
        self.screen = pygame.display.set_mode((windowHeight, windowWidth))
        self.screen.fill(self.white)
        self.generateInitRandom()

    def move(self):  # mve obj to random empty space
        for i in range(self.gridHeight):
            self.debug()
            for j in range(self.gridWidth):
                if self.layout[i, j].figure != 0:
                    nextStep = self.checkNextStep(i, j)

                    if nextStep != 0:
                        # print(nextStep[0], nextStep[1])
                        # print("before: ", self.layout[nextStep[0], nextStep[1]].figure)
                        self.layout[nextStep[0], nextStep[1]] = self.layout[i][j]
                        # print("after: ", self.layout[nextStep[0], nextStep[1]].figure)
                        self.layout[i, j].figure = 0

        exit()

    def checkNextStep(self, i, j):
        if i - 1 >= 0 and self.layout[i - 1, j].figure == 0:
            return (i - 1, j)
        elif j - 1 >= 0 and self.layout[i, j - 1].figure == 0:
            return (i, j - 1)
        elif j + 1 < self.gridWidth and self.layout[i, j + 1].figure == 0:
            return (i, j + 1)
        elif i + 1 < self.gridHeight and self.layout[i + 1, j].figure == 0:
            return (i + 1, j)
        else:
            return 0

    def checkSurrounding(self, i, j,
                         target):  # check surrounding objects has infect on current object, target is a tuple
        for _i in range(-1, 2, 1):
            for _j in range(-1, 2, 1):
                if (0 <= i + _i < self.gridHeight) and (0 <= j + _j < self.gridWidth) and self.layout[
                    i + _i, j + _j].figure in target:
                    return (i + _i, j + _j)
        return 0

    def updateLayout(self):
        for i in range(self.gridHeight):
            for j in range(self.gridWidth):
                rect = pygame.Rect(j * self.blockSize, i * self.blockSize, self.blockSize, self.blockSize)
                # print(i, j, self.layout[i, j].figure)
                pygame.draw.rect(self.screen, self.layout[i, j].color, rect)

    def updateObjCondition(self):
        for i in range(self.gridHeight):
            for j in range(self.gridWidth):
                if self.layout[i, j].figure == 0:  # empty
                    continue
                elif self.layout[i, j].figure == 1:  # man
                    pass
                    targetObjCoor = self.checkSurrounding(i, j, (2, -1))
                    if targetObjCoor != 0:
                        self.layout[targetObjCoor[0], targetObjCoor[1]].figure = 5
                    # Person(0) problem: location to find empty space put new create obj
                elif self.layout[i, j].figure == 2:  # woman
                    pass
                    targetObjCoor = self.checkSurrounding(i, j, (1, -1))
                    if targetObjCoor != 0:
                        self.layout[targetObjCoor[0], targetObjCoor[1]].figure = 4
                    # problem: location to find empty space put new create obj
                elif self.layout[i, j].figure == 3:  # coach
                    targetObjCoor = self.checkSurrounding(i, j, (4, 5))
                    if targetObjCoor != 0:
                        if self.layout[targetObjCoor[0], targetObjCoor[1]].figure == 4:
                            self.layout[targetObjCoor[0], targetObjCoor[1]].figure = 2
                        else:
                            self.layout[targetObjCoor[0], targetObjCoor[1]].figure = 1
                elif self.layout[i, j].figure == 4:  # fat girl
                    targetObjCoor = self.checkSurrounding(i, j, (3, -1))
                    if targetObjCoor != 0:
                        self.layout[i, j].figure = 2

                elif self.layout[i, j].figure == 5:  # fat boy
                    targetObjCoor = self.checkSurrounding(i, j, (3, -1))
                    if targetObjCoor != 0:
                        self.layout[i, j].figure = 1
                self.layout[i, j].colorUpdate()

    def generateInitRandom(self):
        self.gridHeight = int(self.windowHeight / self.blockSize)
        self.gridWidth = int(self.windowWidth / self.blockSize)
        objQuantity = int(pow(self.gridWidth, 2))

        self.objIndiceList = [0, 1, 2, 3, 4,
                              5]  # val (0, 1, 2, 3, 4, 5) means (gymSpace, man, woman, coach, fat_girl, fat_boy)
        self.objLocList = np.random.choice(self.objIndiceList, objQuantity,
                                           p=[self.gymSpaceRatio, self.manRatio, self.womanRatio, self.trainerRatio,
                                              self.fatWomanRatio, self.fatManRatio])
        self.objLocList = self.objLocList.reshape((self.gridHeight, self.gridWidth))
        self.layout = np.empty([100, 100], dtype=object)

        for i in range(self.gridHeight):
            for j in range(self.gridWidth):
                self.layout[i, j] = Person(i, j, self.objLocList[i, j])

    def debug(self):
        arr = np.zeros((self.gridHeight, self.gridWidth), int)
        for i in range(self.gridHeight):
            for j in range(self.gridWidth):
                arr[i, j] = self.layout[i, j].figure

        print(arr)


def main():
    windowHeight = 400
    windowWidth = 400
    blockSize = 20

    global clock
    pygame.init()
    clock = pygame.time.Clock()
    gym = Gym(windowHeight, windowWidth, blockSize)

    gym.debug()

    while True:
        # gym.move()
        # gym.debug()
        # return\
        gym.updateObjCondition()

        gym.updateLayout()

        # gym.debug()

        # return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # gym.debug()
        pygame.display.update()
        time.sleep(1)


if __name__ == "__main__":
    main()
