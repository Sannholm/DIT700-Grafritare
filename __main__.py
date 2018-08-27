import pygame
import math


SCREEN_SIZE = (640, 480)

def f(x):
    return math.sin(x)


def coord_to_pxl(coordinate, min, max):
    x_range = max[0] - min[0];
    y_range = max[1] - min[1];
    size_x = int(SCREEN_SIZE[0] / x_range)
    size_y = int(SCREEN_SIZE[1] / y_range)
    trans_coord = ((coordinate[0] - min[0]) * size_x, (coordinate[1] - min[1]) * size_y)

    x = int(trans_coord[0])
    y = int(SCREEN_SIZE[1] - trans_coord[1])
    return (x, y)


def x_pxl_to_coord(x, min, max):
    x_range = max - min;
    trans_x = x + min
    return (x + min ) * (x_range / SCREEN_SIZE[0])


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
            min = (0, -5)
            max = (10, 5)
            for idx in range(SCREEN_SIZE[0]):
                x = x_pxl_to_coord(idx, min[0], max[0])
                y = f(x)
                line_coords.append(coord_to_pxl((x, y), min, max))

            pygame.draw.lines(screen, (255, 255, 255), False, line_coords)
            pygame.display.update()
            done_drawing = True



if __name__ == '__main__':
    main()