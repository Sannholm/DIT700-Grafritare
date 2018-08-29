import pygame
import math
import random

SCREEN_SIZE = (640, 480)
MIN = (random.uniform(-5, -10), random.uniform(-5, -10))
MAX = (random.uniform(5, 10), random.uniform(5, 10))

FONT = None
SCREEN = None

class Function:
    def __init__(self, func, color):
        self.func = func
        self.color = color

    def __call__(self, x):
        return self.func(x)


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

def is_zero(coord, range):
    return math.isclose(coord, 0, abs_tol = range / 10)
def format_number(coord, range):
    if range > 10000 or (not is_zero(coord, range) and abs(coord) < 0.001):
        return "%.0E" % coord

    num_decimals = 0 
    decimal_iter = abs(coord)
    while not is_zero(coord, range) and decimal_iter < 1:
        decimal_iter *= 10 
        num_decimals += 1
    return ("%%.%sf" % num_decimals) % coord

def dict_from_module(module):
    context = {}
    for attr in dir(module):
        context[attr] = getattr(module, attr)

    return context

# We need to create the lambda in a separate function to isolate the scope from the iteration loop below
def create_eval_lambda(func_line):
    return lambda vars: eval(func_line, dict_from_module(math), vars) 

def load_functions_from_file(path):
    functions = []
    with open(path, "r") as file:
        lines = file.readlines()
        if len(lines) % 2 != 0:
            raise Exception("Uneven number of lines in file %d", len(lines))
        for n in range(0, len(lines), 2):
            try:
                color_line = lines[n]
                colors = color_line.split()
                if len(colors) != 3:
                    raise Exception("Color format should be 255 255 255")
                color_arr = list(map(lambda color_str: int(color_str), colors))
                func_line = lines[n + 1]
                func_closure = create_eval_lambda(func_line)
                test_result = func_closure({ "x": 0.0, "time": pygame.time.get_ticks() / 1000.0 })
                functions.append(Function(func_closure, color_arr))
            except Exception as error:
                print("Function " + lines[n + 1] + " error: " + str(error))

    return functions

def main():
    pygame.init()

    pygame.display.set_caption('Expanded Brain')

    global FONT
    FONT = pygame.font.SysFont(None, 16)
    global SCREEN
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)

    file_path = "functions.txt"

    functions = []

    running = True

    frame_number = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if frame_number % 30 == 0:
            try:
                functions = load_functions_from_file(file_path)
            except Exception as error:
                print(error)

        SCREEN.fill((0,0,0))
        axis_color = (70, 70, 70)
        grid_color = (30, 30, 30)
        marker_color = (70, 70, 70)

        window_x = MAX[0] - MIN[0]
        x_grid_spacing = 1000000000
        while window_x / x_grid_spacing <= 2:
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
            if is_zero(x_coord, x_grid_spacing):
                text_coord = (marker_pixel_coord[0] + 10, marker_pixel_coord[1] + 5)

            render_text(format_number(x_coord, x_grid_spacing), text_coord, marker_color, (0.5, 0))

        window_y = MAX[1] - MIN[1]
        y_grid_spacing = 1000000000
        while window_y / y_grid_spacing <= 3:
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

            if not is_zero(y_coord, y_grid_spacing):
                text_coord = (marker_pixel_coord[0] - 5, marker_pixel_coord[1])
                render_text(format_number(y_coord, y_grid_spacing), text_coord, marker_color, (1, 0.5))

        pygame.draw.line(SCREEN, axis_color,
                        coord_to_pxl((0, MIN[1]), MIN, MAX),
                        coord_to_pxl((0, MAX[1]), MIN, MAX))
        pygame.draw.line(SCREEN, axis_color,
                        coord_to_pxl((MIN[0], 0), MIN, MAX),
                        coord_to_pxl((MAX[0], 0), MIN, MAX))

        for function in functions:
            line_coords = []
            for idx in range(SCREEN_SIZE[0]):
                x = x_pxl_to_coord(idx, MIN[0], MAX[0])
                y = function({ "x": x, "time": pygame.time.get_ticks() / 1000.0 })
                line_coords.append(coord_to_pxl((x, y), MIN, MAX))

            pygame.draw.lines(SCREEN, function.color, False, line_coords)

        pygame.display.update()

        frame_number += 1


if __name__ == '__main__':
    main()