import pygame
import sys
import constants


def initialize_game():
    pygame.init()
    surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption(constants.TITLE)
    surface.fill(constants.WHITE)
    return surface


def read_board(gridfile):
    with open(gridfile, "r") as f:
        board_map = f.readlines()
    board_map = [line.strip() for line in board_map]
    return board_map


def get_space_color(space_contents):
    space_color = constants.DARKLAVA
    if space_contents == "X":
        space_color = constants.PASTELBROWN
    if space_contents == "-":
        space_color = constants.PALETAUPE
    return space_color


def draw_board(surface, grid_spaces):
    for j, space in enumerate(grid_spaces):
        for i, space_contents in enumerate(space):
            #print("{},{}: {}".format(i, j, space_contents))
            myrect = pygame.Rect(i*constants.BLOCK_WIDTH, j*constants.BLOCK_HEIGHT, constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
            pygame.draw.rect(surface, get_space_color(space_contents), myrect)


def draw_lines(surface):
    for i in range(constants.GRID_ROWS):
        new_height = round(i * constants.BLOCK_HEIGHT)
        new_width = round(i * constants.BLOCK_WIDTH)
        pygame.draw.line(surface, constants.DARKLAVA, (0, new_height), (constants.SCREEN_WIDTH, new_height), 2)
        pygame.draw.line(surface, constants.DARKLAVA, (new_width, 0), (new_width, constants.SCREEN_HEIGHT), 2)

def game_loop(surface, board_grid):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()
        draw_board(surface, board_grid)
        draw_lines(surface)
        pygame.display.update()


def main():
    board_map = read_board(constants.GRIDFILE)
    surface = initialize_game()
    game_loop(surface, board_map)
"""
pyg.init()



# wood background
woodImage = pyg.image.load("wood_board.jpg")


def wood(x, y):
    surface.blit(woodImage, (x, y))


x = (screen_width // 2000)
y = (screen_height // 2000)


"""

if __name__ == "__main__":
    main()