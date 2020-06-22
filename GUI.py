import pygame as pyg
from sys import exit


pyg.init()

# screen
screen_width = 650
screen_height = 550

# colors
white = (255, 255, 255)
black = (0, 0, 0)

# wood background
woodImage = pyg.image.load("wood_board.jpg")


surface = pyg.display.set_mode((screen_width, screen_height))
pyg.display.set_caption("Gess Game")
surface.fill(white)

def wood(x, y):
    surface.blit(woodImage, (x, y))

pyg.Surface.scroll()
# close window by clicking X
while True:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            exit()
        if event.type == pyg.KEYDOWN:
            pyg.quit()
            exit()
    pyg.display.update()



