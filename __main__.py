import pygame
import math


SCREEN_SIZE = (640, 480)
SCALE = 10

def f(x):
    return math.tan(x) * math.sin(x)


def coord_to_pxl(coordinate, scale = 10):
    size_x = int(SCREEN_SIZE[0] / 2 / scale)
    size_y = int(SCREEN_SIZE[1] / 2 / scale)
    trans_coord = (coordinate[0] * size_x, coordinate[1] * size_y)

    x = int(trans_coord[0] + SCREEN_SIZE[0] / 2)
    y = int(SCREEN_SIZE[1] / 2- trans_coord[1])
    return (x, y)


def x_pxl_to_coord(x, scale = 10):
    trans_x = x - int(SCREEN_SIZE[0] / 2)
    size_x = int(SCREEN_SIZE[0] / 2 / scale)
    return trans_x / size_x


def main():
    pygame.init()

    pygame.display.set_caption('Expanded Brain')

    screen = pygame.display.set_mode(SCREEN_SIZE)
    running = True
    done_drawing = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not done_drawing:
            line_coords = []
            for idx in range(SCREEN_SIZE[0]):
                x = x_pxl_to_coord(idx, SCALE)
                y = f(x)
                line_coords.append(coord_to_pxl((x, y)))

            pygame.draw.lines(screen, (255, 255, 255), False, line_coords)
            pygame.display.update()
            done_drawing = True



if __name__ == '__main__':
    main()