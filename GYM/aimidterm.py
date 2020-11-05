import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy.random import seed
from numpy.random import randint
import pygame


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

class Person:
    def __init__(self, x, y, figure):
        self.x = x
        self.y = y
        self.figure = figure
        self.nextSecondChangeFigure = None
        self.white = (255, 255, 255)  # grid background
        self.black = (0, 0, 0)  # personal trainer
        self.pink = (255, 105, 180)  # fat woman
        self.purple = (102, 0, 102)  # fat man
        self.blue = (0, 0, 255)  # man
        self.red = (255, 0, 0)  # woman
        self.green = (0, 255, 0)  # personal trainer
        if figure == 0:
            self.color = self.white
        elif figure == 1:
            self.color = self.blue
        elif figure == 2:
            self.color = self.red
        elif figure == 3:
            self.color = self.green
        elif figure == 4:
            self.color = self.pink
        elif figure == 5:
            self.color = self.purple

    def move(self):
        pass


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
        self.manRatio = 0.2
        self.womanRatio = 0.2
        self.fatManRatio = 0.025
        self.fatWomanRatio = 0.025
        self.trainerRatio = 0.05
        self.gymSpaceRatio = 0.5
        self.screen = pygame.display.set_mode((windowHeight, windowWidth))
        self.screen.fill(self.white)
        self.drawGrid()
        self.generateInitRandom()

    def update(self):
        pass

    def generateInitRandom(self):
        objQuantity = int(pow(self.windowHeight / self.blockSize, 2))

        self.objIndiceList = [0, 1, 2, 3, 4,
                              5]  # val (0, 1, 2, 3, 4, 5) means (gymSpace, man, woman, coach, fat_girl, fat_boy)
        self.objLocList = np.random.choice(self.objIndiceList, objQuantity,
                                           p=[self.gymSpaceRatio, self.manRatio, self.womanRatio, self.trainerRatio,
                                              self.fatWomanRatio, self.fatManRatio])
        self.objLocList = self.objLocList.reshape(
            (int(self.windowHeight / self.blockSize), int(self.windowWidth / self.blockSize)))

        for i in range(int(self.windowHeight / self.blockSize)):
            for j in range(int(self.windowWidth / self.blockSize)):
                self.objLocList[i, j] = Person(i, j, self.objLocList[i, j])

    def nextMoveCheck(self):
        pass

    def drawGrid(self):
        self.blockSize = 20  # Set the size of the grid block
        for i in range(self.windowHeight):
            for j in range(self.windowWidth):
                rect = pygame.Rect(j * self.blockSize, i * self.blockSize, self.blockSize,
                                   self.blockSize)  # left, top, width, height
                pygame.draw.rect(self.screen, self.black, rect, 1)


def operationOfCurrentPoint(sumOfSurviver, i, j):
    if (orgGrid[i, j] == 255):  # current point survive
        if (sumOfSurviver <= 1):
            tmpGrid[i, j] = 0
        elif (sumOfSurviver <= 3):
            pass
        else:
            tmpGrid[i, j] = 0
    else:
        if (sumOfSurviver == 3):
            tmpGrid[i, j] = 255
        else:
            pass


def checkSurrounding(i, j):  # checking sorrounding surviver
    sumOfSurviver = 0

    if (i - 1 >= 0 and j - 1 >= 0 and orgGrid[i - 1, j - 1] == 255):  # left-up
        sumOfSurviver += 1
    if (i - 1 >= 0 and orgGrid[i - 1, j] == 255):  # up
        sumOfSurviver += 1
    if (i - 1 >= 0 and j + 1 < gridSize and orgGrid[i - 1, j + 1] == 255):  # right-up
        sumOfSurviver += 1
    if (j - 1 >= 0 and orgGrid[i, j - 1] == 255):  # left
        sumOfSurviver += 1
    if (j + 1 < gridSize and orgGrid[i, j + 1] == 255):  # right
        sumOfSurviver += 1
    if (i + 1 < gridSize and j - 1 >= 0 and orgGrid[i + 1, j - 1] == 255):  # left-down
        sumOfSurviver += 1
    if (i + 1 < gridSize and orgGrid[i + 1, j] == 255):  # down
        sumOfSurviver += 1
    # right-down
    if (i + 1 < gridSize and j + 1 < gridSize and orgGrid[i + 1, j + 1] == 255):
        sumOfSurviver += 1

    operationOfCurrentPoint(sumOfSurviver, i, j)


def update(self):  # update the current mat
    # sumOfSurviver = 0
    global orgGrid, tmpGrid
    tmpGrid = orgGrid.copy()
    for i in range(gridSize):
        for j in range(gridSize):
            checkSurrounding(i, j)

    mat.set_data(tmpGrid)
    orgGrid = tmpGrid
    return [mat]


def main():
    windowHeight = 400
    windowWidth = 400
    blockSize = 20

    global clock
    pygame.init()
    clock = pygame.time.Clock()
    gym = Gym(windowHeight, windowWidth, blockSize)

    while True:
        gym.drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

    '''
    global mat, orgGrid, gridSize

    gridSize = 300
    vals = [255, 0]
    orgGrid = np.random.choice(
        vals, gridSize*gridSize, p=[0.2, 0.8]).reshape(gridSize, gridSize)

    # below draw the figure
    figure, axes = plt.subplots()
    mat = axes.matshow(orgGrid)
    ani = animation.FuncAnimation(figure, update, interval=50, save_count=50)
    plt.show()
    '''


if __name__ == "__main__":
    main()
