import pygame
import random
import sys
import time



class Colors:
    def __init__(self):
        self.grid = "#cccccc"
        self.pause = "#213d69"
        self.dead = "#ffffff"
        self.deadHover = "#c7c7c7"
        self.alive = "#34ebcf"
        self.aliveHover = "#209685"



class Cell:
    def __init__(self):
        self.alive = False


    def posX(self, j, size):
        return j*(size+1)+1


    def posY(self, i, size):
        return i*(size+1)+1


    def draw(self, window, pause, colors, i, j, size):
        color = None

        if self.alive:
            color = colors.alive
        else:
            color = colors.dead

        if pause:
            pos = pygame.mouse.get_pos()
            if self.isCursor(pos[0], pos[1], i, j, size):
                if self.alive:
                    color = colors.aliveHover
                else:
                    color = colors.deadHover
        
        cellRect = pygame.rect.Rect(self.posX(j, size), self.posY(i, size), size, size)
        pygame.draw.rect(window, color, cellRect)


    def isCursor(self, posX, posY, i, j, size):
        if (posX >= self.posX(j, size) and posX <= self.posX(j, size)+size) and (posY >= self.posY(i, size) and posY <= self.posY(i, size)+size):
            return True
        else:
            return False
    

    def changeAlive(self):
        self.alive = not self.alive



class Board:
    def __init__(self, columns, rows, cellSize, infinite):
        self.columns = columns
        self.rows = rows
        self.cellSize = cellSize
        self.cells = [[Cell() for _ in range(self.columns)] for _ in range(self.rows)]
        self.infinite = infinite
    

    def clear(self):
        self.cells = [[Cell() for _ in range(self.columns)] for _ in range(self.rows)]


    def randomize(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                self.cells[i][j].alive = random.choice([True, False])


    def nextGen(self, speed):
        nextCells = [[Cell() for _ in range(self.columns)] for _ in range(self.rows)]

        for i in range(0, self.rows):
            for j in range(0, self.columns):
                aliveNeighbours = 0

                for k in range(0, 3):
                    for l in range(0, 3):
                        if not(k==1 and l==1):
                            if self.infinite:
                                if self.cells[(i+k-1)%self.rows][(j+l-1)%self.columns].alive:
                                        aliveNeighbours += 1
                            else:
                                try:
                                    if self.cells[i+k-1][j+l-1].alive:
                                        aliveNeighbours += 1
                                except:
                                    pass
                
                if self.cells[i][j].alive and (aliveNeighbours == 2 or aliveNeighbours == 3):
                    nextCells[i][j].alive = True
                elif self.cells[i][j].alive == False and aliveNeighbours == 3:
                    nextCells[i][j].alive = True
                else:
                    nextCells[i][j].alive = False

        self.cells = nextCells
        time.sleep(speed)
    

    def draw(self, window, pause, colors):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                self.cells[i][j].draw(window, pause, colors, i, j, self.cellSize)



class App:
    def __init__(self, columns, rows, cellSize, colors, infinite):
        self.board = Board(columns, rows, cellSize, infinite)
        self.pause = True
        self.speed = 0.3
        self.colors = colors
        self.toChange = None
        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode([self.board.columns*(self.board.cellSize+1)+1, self.board.rows*(self.board.cellSize+1)+1])
        pygame.display.set_caption("Game of Life")


    def checkMouseClick(self, clickX, clickY, alive):
        for i in range(0, self.board.rows):
            for j in range(0, self.board.columns):
                if self.board.cells[i][j].isCursor(clickX, clickY, i, j, self.board.cellSize) and alive == self.board.cells[i][j].alive:
                    self.board.cells[i][j].changeAlive()


    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_SPACE:
                    if self.pause:
                        self.pause = False
                    else:
                        self.pause = True

                elif event.key == pygame.K_TAB and self.pause:
                        self.board.randomize()

                elif event.key == pygame.K_BACKSPACE and self.pause:
                        self.board.clear()

                elif event.key == pygame.K_RETURN: 
                    self.speed = 0.5

                elif event.key == pygame.K_UP:
                    self.speed -= 0.05
                    if self.speed < 0: 
                            self.speed = 0

                elif event.key == pygame.K_DOWN:
                    self.speed += 0.05


    def showPause(self):
        pause = pygame.font.SysFont("arial", 15).render("PAUSE", True, self.colors.pause)
        self.window.blit(pause, (5, 5))


    def draw(self):
        self.window.fill(self.colors.grid)
        self.board.draw(self.window, self.pause, self.colors)



    def run(self):
        while True:
            self.checkEvent()
            self.draw()

            if self.pause:
                self.showPause()

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    self.checkMouseClick(pos[0], pos[1], False)

                elif pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    self.checkMouseClick(pos[0], pos[1], True)

            else:
                self.board.nextGen(self.speed)
        
            pygame.display.flip()



if __name__ == "__main__":
    app = App(40, 40, 20, Colors(), True)
    app.run()