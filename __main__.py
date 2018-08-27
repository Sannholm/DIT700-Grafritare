import pygame
import math
import random

SCREEN_SIZE = (640, 480)
MIN = (random.uniform(-50, -10), random.uniform(-50, -10))
MAX = (random.uniform(10, 50), random.uniform(10, 50))

FONT = None
SCREEN = None

def f(x):
    return math.sin(x)


def coord_to_pxl(coordinate, min, max):
    x_range = max[0] - min[0]
    y_range = max[1] - min[1]
    size_x = SCREEN_SIZE[0] / x_range
    size_y = SCREEN_SIZE[1] / y_range
    trans_coord = ((coordinate[0] - min[0]) * size_x, (coordinate[1] - min[1]) * size_y)

    x = trans_coord[0]
    y = SCREEN_SIZE[1] - trans_coord[1]
    return (x, y)


def x_pxl_to_coord(x, min, max):
    x_range = max - min
    return x * (x_range / SCREEN_SIZE[0]) + min

def render_text(text, coord, color, alignment=(0,0)):
    text = FONT.render(text, True, color)
    textrect = text.get_rect()
    textrect.x = -textrect.width * alignment[0] + coord[0]
    textrect.y = -textrect.height * alignment[1] + coord[1]

    SCREEN.blit(text, textrect)


def main():
    pygame.init()

    pygame.display.set_caption('Expanded Brain')

    global FONT
    FONT = pygame.font.SysFont(None, 16)
    global SCREEN
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)

    running = True
    done_drawing = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not done_drawing:
            axis_color = (70, 70, 70)
            grid_color = (30, 30, 30)
            marker_color = (70, 70, 70)

            window_x = MAX[0] - MIN[0]
            x_grid_spacing = 1000000000
            while window_x / x_grid_spacing < 1:
                x_grid_spacing /= 10

            num_lines = int(window_x / x_grid_spacing)
            for x in range(1, num_lines + 1):
                x_coord = MIN[0] + x * x_grid_spacing - MIN[0] % x_grid_spacing
                pygame.draw.line(SCREEN, grid_color,
                                 coord_to_pxl((x_coord, MIN[1]), MIN, MAX),
                                 coord_to_pxl((x_coord, MAX[1]), MIN, MAX))

                marker_pixel_coord = coord_to_pxl((x_coord, 0), MIN, MAX)
                pygame.draw.line(SCREEN, marker_color,
                                 marker_pixel_coord,
                                 (marker_pixel_coord[0], marker_pixel_coord[1] - 10))

                text_coord = (marker_pixel_coord[0], marker_pixel_coord[1] + 5)
                if x_coord == 0:
                    text_coord = (marker_pixel_coord[0] + 10, marker_pixel_coord[1] + 5)
                render_text("%.0f" % x_coord, text_coord, marker_color, (0.5, 0))

            window_y = MAX[1] - MIN[1]
            y_grid_spacing = 1000000000
            while window_y / y_grid_spacing < 1:
                y_grid_spacing /= 10

            num_lines = int(window_y / y_grid_spacing)
            for y in range(1, num_lines + 1):
                y_coord = MIN[1] + y * y_grid_spacing - MIN[1] % y_grid_spacing
                pygame.draw.line(SCREEN, grid_color,
                                 coord_to_pxl((MIN[0], y_coord), MIN, MAX),
                                 coord_to_pxl((MAX[0], y_coord), MIN, MAX))

                marker_pixel_coord = coord_to_pxl((0, y_coord), MIN, MAX)
                pygame.draw.line(SCREEN, marker_color,
                                 marker_pixel_coord,
                                 (marker_pixel_coord[0] + 10, marker_pixel_coord[1]))

                if y_coord != 0:
                    text_coord = (marker_pixel_coord[0] - 5, marker_pixel_coord[1])
                    render_text("%.0f" % y_coord, text_coord, marker_color, (1, 0.5))

            pygame.draw.line(SCREEN, axis_color,
                             coord_to_pxl((0, MIN[1]), MIN, MAX),
                             coord_to_pxl((0, MAX[1]), MIN, MAX))
            pygame.draw.line(SCREEN, axis_color,
                             coord_to_pxl((MIN[0], 0), MIN, MAX),
                             coord_to_pxl((MAX[0], 0), MIN, MAX))

            line_coords = []
            for idx in range(SCREEN_SIZE[0]):
                x = x_pxl_to_coord(idx, MIN[0], MAX[0])
                y = f(x)
                line_coords.append(coord_to_pxl((x, y), MIN, MAX))

            pygame.draw.lines(SCREEN, (255, 255, 255), False, line_coords)
            pygame.display.update()
            done_drawing = True



if __name__ == '__main__':
    main()