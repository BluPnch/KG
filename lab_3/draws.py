CANVAS_WIDTH = 990
CANVAS_HEIGHT = 823

SIZE = 1

from math import *


def dspectrum(canvas, degree, line_color, dline_func, x_center, y_center, line_length):
    # num_lines = int(360 / degree)
    i = 0
    while i < 360:
        x_end = x_center + line_length * cos(radians(i))
        y_end = y_center - line_length * sin(radians(i))
        dline_func(canvas, x_center, y_center, int(x_end), int(y_end), line_color)
        i += degree

def add_background(canvas, bg_color):
    bg_rect = canvas.find_withtag("bg_rect")
    if bg_rect:
        canvas.itemconfig(bg_rect, fill=bg_color)
    else:
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=bg_color, width=0,
                                tags="bg_rect")


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0


def draw_pixel(canvas, x, y, color):
    x *= SIZE
    y *= SIZE

    # canvas.create_line(x, y, x + SIZE, y + SIZE, fill=color)
    canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=color, outline="")


def change_intensivity(intens, hex_color):
    if not 0 <= intens <= 1:
        intens = 1
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = 255 * (1 - intens) + r * intens
    g = 255 * (1 - intens) + g * intens
    b = 255 * (1 - intens) + b * intens
    color = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
    return color


# __________________________________________________________________
# использующий библиотечную функцию

def dline_biblio(canvas, x1, y1, x2, y2, line_color):
    canvas.create_line(x1, y1, x2, y2, fill=line_color)


# __________________________________________________________________
# цифрового дифференциального анализатора


def dline_CDA(canvas, x1, y1, x2, y2, line_color):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        l = abs(dx)
    else:
        l = abs(dy)
    dx /= l
    dy /= l
    x, y = x1, y1

    for i in range(0, int(l) + 1):
        draw_pixel(canvas, round(x), round(y), line_color)
        # высвечивание пикселя (E(x), E(y)) #E - операция округления (медленная)
        x += dx
        y += dy


# __________________________________________________________________
# Брезенхема с действительными данными

# Ошибка - расстояние от т идеального отрезка до ближайшего пикселя
# Одна из координат всегда изменяется на +- 1, вторая либо остается неизм, либо изменяется на +- 1???

def dline_Brezen_float(canvas, x1, y1, x2, y2, line_color):
    dx = x2 - x1
    dy = y2 - y1
    sx = sign(dx)
    sy = sign(dy)

    dx, dy = abs(dx), abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        swap = 1
    else:
        swap = 0

    m = dy / dx
    e = m - 1 / 2
    x, y = x1, y1

    for i in range(0, int(dx) + 1):
        draw_pixel(canvas, x, y, line_color)
        if e >= 0:
            if not swap:
                y += sy
            else:
                x += sx
            e -= 1
        if not swap:
            x += sx
        else:
            y += sy

        e += m


# __________________________________________________________________
# Брезенхема с целочисленными данными
def dline_Brezen_int(canvas, x1, y1, x2, y2, line_color):
    dx = x2 - x1
    dy = y2 - y1
    sx = sign(dx)
    sy = sign(dy)

    dx, dy = abs(dx), abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        swap = 1
    else:
        swap = 0

    # e = dy / dx - 1/2
    # 2*dx * e = 2*dy - dx
    e = 2 * dy - dx
    x, y = x1, y1

    for i in range(0, int(dx) + 1):
        draw_pixel(canvas, x, y, line_color)
        if e >= 0:
            if not swap:
                y += sy
            else:
                x += sx
            e -= (2 * dx)
        if not swap:
            x += sx
        else:
            y += sy

        e += (2 * dy)


# __________________________________________________________________
# Брезенхема с устранением ступенчатости

def dline_Brezen_no_jaggies(canvas, x1, y1, x2, y2, line_color):
    I = 1
    dx = x2 - x1
    dy = y2 - y1
    sx = sign(dx)
    sy = sign(dy)

    dx, dy = abs(dx), abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        swap = 1
    else:
        swap = 0

    m = (I * dy) / dx
    w = I - m
    e = I / 2

    x, y = x1, y1

    for i in range(0, int(dx)):
        color = change_intensivity(e, line_color)
        draw_pixel(canvas, x, y, color)
        if e < w:
            if not swap:
                x += sx
            else:
                y += sy
            e += m
        else:
            x += sx
            y += sy
            e -= w


# __________________________________________________________________
# Ву

def ipart(x):
    # Возвращает целую часть от x
    return int(x)


def round(x):
    # Округляет x до ближайшего целого
    return ipart(x + 0.5)


def fpart(x):
    # Возвращает дробную часть x
    return x - ipart(x)


def dline_Wu(canvas, x1, y1, x2, y2, line_color):
    swap = abs(y2 - y1) > abs(x2 - x1)

    if swap:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x2 < x1:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        grad = 1
    else:
        grad = dy / dx

    # начальную точку
    x_end, y_end = x1, y1
    x_1 = x_end  # Будет использоваться в основном цикле
    y_1 = ipart(y_end)
    color_1 = line_color
    if swap:
        draw_pixel(canvas, y_1, x_1, color_1)
    else:
        draw_pixel(canvas, x_1, y_1, color_1)
    intery = y_end + grad

    # конечную точку
    x_end, y_end = x2, y2
    x_2 = x_end
    y_2 = ipart(y_end)
    color_1 = line_color
    if swap:
        draw_pixel(canvas, y_2, x_2, color_1)
    else:
        draw_pixel(canvas, x_2, y_2, color_1)

    if swap:
        for x in range(int(x_1), int(x_2) + 1):
            color_1 = change_intensivity((1 - fpart(intery)), line_color)
            color_2 = change_intensivity(fpart(intery), line_color)
            draw_pixel(canvas, ipart(intery), x, color_1)
            draw_pixel(canvas, ipart(intery) + 1, x, color_2)
            intery += grad
    else:
        for x in range(int(x_1), int(x_2) + 1):
            color_1 = change_intensivity((1 - fpart(intery)), line_color)
            color_2 = change_intensivity(fpart(intery), line_color)
            draw_pixel(canvas, x, ipart(intery), color_1)
            draw_pixel(canvas, x, ipart(intery) + 1, color_2)
            intery += grad
