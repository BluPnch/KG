# Вавилова Варвара ИУ7-44Б
# Перенос, масштабирование и поворот рисунка
from time import perf_counter
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageTk

from errors import *
from draws import *

FONT = 13
PIXELS_IN_LINE = 150
COUNT_MEASURES = 100

window = Tk()  # создаем окошко
window.title("")
# window.geometry('1412x820+60+0')


screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")
# window.attributes('-fullscreen', True)

# CANVAS
canvas = Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="white")
canvas.grid(column=7, row=0, columnspan=23, rowspan=20, sticky=NSEW)
ghost_canvas = Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="white")

def choose_color_bg():
    color = colorchooser.askcolor(title="Выберите цвет:")
    if color[1]:  # если цвет выбран
        button_bg_color.config(bg=color[1])  # обновляем фон кнопки


def choose_color_line():
    color = colorchooser.askcolor(title="Выберите цвет:")
    if color[1]:  # если цвет выбран
        button_line_color.config(bg=color[1])  # обновляем фон кнопки


def canvas_clear():
    canvas.delete("all")


# ____________________________________________________________________________

def choice_rendering():
    if VAR.get() == 1:
        dline_func = dline_biblio
    elif VAR.get() == 2:
        dline_func = dline_CDA
    elif VAR.get() == 3:
        dline_func = dline_Brezen_float
    elif VAR.get() == 4:
        dline_func = dline_Brezen_int
    elif VAR.get() == 5:
        dline_func = dline_Brezen_no_jaggies
    else:
        dline_func = dline_Wu
    return dline_func


def draw_line(x1, y1, x2, y2):
    line_color = button_line_color.cget('bg')
    bg_color = button_bg_color.cget('bg')
    add_background(canvas, bg_color)

    dline_func = choice_rendering()
    dline_func(canvas, x1, y1, x2, y2, line_color)


def draw_spectrum(degree, x_center, y_center, line_length):
    line_color = button_line_color.cget('bg')
    bg_color = button_bg_color.cget('bg')
    add_background(canvas, bg_color)

    dline_func = choice_rendering()
    dspectrum(canvas, degree, line_color, dline_func, x_center, y_center, line_length)


def push_button_draw_line():
    try:
        x1 = int(x1_entry.get())
        y1 = int(y1_entry.get())
        try:
            x2 = int(x2_entry.get())
            y2 = int(y2_entry.get())

            draw_line(x1, y1, x2, y2)

        except ValueError:
            if x2_entry.get() == "" or y2_entry.get() == "":
                error_empty_data()
            else:
                error_invalid_data()
    except ValueError:
        if x1_entry.get() == "" or y1_entry.get() == "":
            error_empty_data()
        else:
            error_invalid_data()


def push_button_draw_spectrum():
    try:
        x_center = int(x_center_entry.get())
        y_center = int(y_center_entry.get())
        try:
            degree = float(degree_entry.get())
            try:
                line_length = int(line_length_entry.get())

                draw_spectrum(degree, x_center, y_center, line_length)

            except ValueError as e:
                print(e)
                if line_length_entry.get() == "":
                    error_empty_length()
                else:
                    error_invalid_length()
        except ValueError:
            if degree_entry.get() == "":
                error_empty_degree()
            else:
                error_invalid_degree()
    except ValueError:
        if x_center_entry.get() == "" or y_center_entry.get() == "":
            error_empty_data()
        else:
            error_invalid_data()

# __________________________________________________________________
# Тестовые данные
def func_measure(func_draw):
    line_colour = "#ffffff"
    start = perf_counter()
    for i in range(COUNT_MEASURES):
        func_draw (ghost_canvas, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, line_colour)
    end = perf_counter()
    ghost_canvas.delete("all")
    return end - start


def time_measure():
    ghost_canvas.delete("all")
    time_biblio = func_measure(dline_biblio)
    time_CDA = func_measure(dline_CDA)
    time_Brezen_float = func_measure(dline_Brezen_float)
    time_Brezen_int = func_measure(dline_Brezen_int)
    time_Brezen_no_jaggies = func_measure(dline_Brezen_no_jaggies)
    time_Wu = func_measure(dline_Wu)

    times = [time_biblio, time_CDA, time_Brezen_float, time_Brezen_int, time_Brezen_no_jaggies, time_Wu]
    algorithms = ['biblio', 'CDA', 'Brezen_float', 'Brezen_int', 'Brezen_no_jaggies', 'Wu']

    plt.title('Замеры времени')
    plt.xlabel('Алгоритмы')
    plt.ylabel('Время')
    plt.bar(algorithms, times, color='skyblue')
    plt.xticks(rotation=25)
    plt.show()


# _______________________________________________________________________


# _______________________________________________________________________
# BUTTON

button_bg_color = Button(window, width=7, bg="#ffffff", command=choose_color_bg)
button_bg_color.grid(column=3, row=0, columnspan=1, sticky="W")
button_line_color = Button(window, width=7, bg="#000000", command=choose_color_line)
button_line_color.grid(column=3, row=1, columnspan=1, sticky="W")

button_search = Button(window, width=15, height='2', text="Очистить холст", command=canvas_clear,
                       font=("Tahoma", FONT - 1))
button_search.grid(column=4, row=0, columnspan=2, rowspan=2)

button_task = Button(window, width=10, height='2', text="Задание", command=show_task, font=("Tahoma", FONT - 1))
button_task.grid(column=0, row=0, columnspan=2, rowspan=2)

button_draw_line = Button(window, width=20, height='1', text="Линия", command=push_button_draw_line,
                          font=("Tahoma", FONT - 1))
button_draw_line.grid(column=0, row=16, columnspan=3)
button_draw_sun = Button(window, width=20, height='1', text="Спектр", command=push_button_draw_spectrum,
                         font=("Tahoma", FONT - 1))
button_draw_sun.grid(column=3, row=16, columnspan=3)

button_search = Button(window, width=30, height='1', text="Исследование", command=time_measure, font=("Tahoma", FONT - 1))
button_search.grid(column=0, row=17, columnspan=6)

# _______________________________________________________________________
# RADIOBUTTON
VAR = IntVar()
VAR.set(1)
rb_biblio = Radiobutton(window, text="  использующий библиотечную функцию;", variable=VAR, value=1,
                        font=("Tahoma", FONT - 1))
rb_CDA = Radiobutton(window, text="  цифрового дифференциального анализатора;", variable=VAR, value=2,
                     font=("Tahoma", FONT - 1))
rb_Brezen_float = Radiobutton(window, text="  Брезенхема с действительными данными;", variable=VAR, value=3,
                              font=("Tahoma", FONT - 1))
rb_Brezen_int = Radiobutton(window, text="  Брезенхема с целочисленными данными;", variable=VAR, value=4,
                            font=("Tahoma", FONT - 1))
rb_Brezen_no_jaggies = Radiobutton(window, text="  Брезенхема с устранением ступенчатости;", variable=VAR, value=5,
                                   font=("Tahoma", FONT - 1))
rb_Vu = Radiobutton(window, text="  Ву", variable=VAR, value=6, font=("Tahoma", FONT - 1))

rb_biblio.grid(column=1, row=10, columnspan=5, sticky=W, ipady=1)
rb_CDA.grid(column=1, row=11, columnspan=5, sticky=W, ipady=1)
rb_Brezen_float.grid(column=1, row=12, columnspan=5, sticky=W)
rb_Brezen_int.grid(column=1, row=13, columnspan=5, sticky=W)
rb_Brezen_no_jaggies.grid(column=1, row=14, columnspan=5, sticky=W)
rb_Vu.grid(column=1, row=15, columnspan=5, sticky=W)

# _______________________________________________________________________
# ENTRY
x1_entry = Entry(window, width=10, font=("Tahoma", FONT))
y1_entry = Entry(window, width=10, font=("Tahoma", FONT))
x2_entry = Entry(window, width=10, font=("Tahoma", FONT))
y2_entry = Entry(window, width=10, font=("Tahoma", FONT))
x_center_entry = Entry(window, width=10, font=("Tahoma", FONT))
y_center_entry = Entry(window, width=10, font=("Tahoma", FONT))
degree_entry = Entry(window, width=10, font=("Tahoma", FONT))
line_length_entry = Entry(window, width=10, font=("Tahoma", FONT))

x1_entry.grid(column=2, row=3, sticky=W)
y1_entry.grid(column=2, row=4, sticky=W)
x2_entry.grid(column=4, row=3, columnspan=2, sticky=E)
y2_entry.grid(column=4, row=4, columnspan=2, sticky=E)
x_center_entry.grid(column=2, row=6, sticky=W)
y_center_entry.grid(column=2, row=7, sticky=W)
degree_entry.grid(column=5, row=7, sticky=W)
line_length_entry.grid(column=5, row=6, sticky=W)

x1_entry.insert(END, "30")
y1_entry.insert(END, "30")
x2_entry.insert(END, "200")
y2_entry.insert(END, "300")
# x_center_entry.insert(END, "85")
# y_center_entry.insert(END, "80")
x_center_entry.insert(END, CANVAS_WIDTH // 2)
y_center_entry.insert(END, CANVAS_HEIGHT // 2)
degree_entry.insert(END, "10")
line_length_entry.insert(END, "450")

# LABEL
colour_bg_label = Label(window, text=f"Цвет фона: ", font=("Tahoma", FONT), anchor="e", justify='left')
colour_line_label = Label(window, text=f"Цвет линии: ", font=("Tahoma", FONT), anchor="e", justify='left')

x1_label = Label(window, width=5, text=f"x1:  ", font=("Tahoma", FONT), anchor="e", justify='left')
y1_label = Label(window, width=5, text=f"y1:  ", font=("Tahoma", FONT), anchor="e", justify='left')
x2_label = Label(window, width=5, text=f"x2:  ", font=("Tahoma", FONT), anchor="e", justify='left')
y2_label = Label(window, width=5, text=f"y2:  ", font=("Tahoma", FONT), anchor="e", justify='left')
x_center_label = Label(window, width=5, text=f"x:  ", font=("Tahoma", FONT), anchor="e", justify='left')
y_center_label = Label(window, width=5, text=f"y:  ", font=("Tahoma", FONT), anchor="e", justify='left')

point_1 = Label(window, width=10, text=f"   Коорд.\n   начала:", font=("Tahoma", FONT), anchor="center", justify='left')
point_2 = Label(window, width=10, text=f"   Коорд.\n   конца: ", font=("Tahoma", FONT), anchor="center", justify='left')
point_center = Label(window, width=10, text=f"    Коорд.\n    центра\n    спектра: ", font=("Tahoma", FONT),
                     anchor="center", justify='left')
degree = Label(window, width=15, text=f"Угол поворота: ", font=("Tahoma", FONT), anchor="w", justify='left')
line_length = Label(window, width=15, text=f"Радиус спектра: ", font=("Tahoma", FONT), anchor="w", justify='left')
algorithm = Label(window, text=f"Алгоритм:", font=("Tahoma", FONT + 2), anchor="center", justify='left')

empty_horiz_1 = Label(window, width=1, text=f" ", font=("Tahoma", FONT))
empty_horiz_2 = Label(window, width=1, text=f" ", font=("Tahoma", FONT))
empty_vertic_1 = Label(window, width=8, text=f" ", font=("Tahoma", FONT))
empty_vertic_2 = Label(window, width=3, text=f" ", font=("Tahoma", FONT))

# _____GRID_____

colour_bg_label.grid(column=2, row=0, columnspan=1, sticky=W)
colour_line_label.grid(column=2, row=1, columnspan=1, sticky=W)

x1_label.grid(column=1, row=3, sticky=EW)
y1_label.grid(column=1, row=4, sticky=EW)
x2_label.grid(column=4, row=3, sticky=W)
y2_label.grid(column=4, row=4, sticky=W)
x_center_label.grid(column=1, row=6, sticky=EW)
y_center_label.grid(column=1, row=7, sticky=EW)

point_1.grid(column=0, row=3, columnspan=1, rowspan=2)
point_2.grid(column=3, row=3, columnspan=1, rowspan=2)
point_center.grid(column=0, row=6, columnspan=1, rowspan=2, sticky=NSEW)
degree.grid(column=3, row=7, columnspan=2)
line_length.grid(column=3, row=6, columnspan=2)
algorithm.grid(column=0, row=9, columnspan=2, sticky=E)

empty_horiz_1.grid(column=0, row=2, columnspan=5, sticky=EW)
empty_horiz_2.grid(column=0, row=8, columnspan=5, sticky=EW)
# empty_vertic_1.grid(column=0, row=0, rowspan=9, sticky=EW)
empty_vertic_2.grid(column=6, row=3, rowspan=19, sticky=EW)




# __________________________________________________________________
# Тестовые данные
'''
r = 200
fi = 82
test = 3, 3, 6, 13
dline_CDA(canvas, *test, '#00ff00')
dline_Brezen_int(canvas, *test, '#000000')

test = 6, 3, 9, 13
dline_Brezen_int(canvas, *test, '#000000')
dline_CDA(canvas, *test, '#00ff00')

test = 9, 3, 12, 13
dline_CDA(canvas, *test, '#00ff00')
dline_Brezen_float(canvas, *test, '#ff0000')

test = 12, 3, 15, 13
dline_Brezen_float(canvas, *test, '#ff0000')
dline_CDA(canvas, *test, '#00ff00')

test = 15, 3, 18, 13
dline_Brezen_int(canvas, *test, '#000000')
dline_Brezen_float(canvas, *test, '#ff0000')

test = 18, 3, 21, 13
dline_Brezen_float(canvas, *test, '#ff0000')
dline_Brezen_int(canvas, *test, '#000000')

test = 24, 3, 27, 13
dline_Brezen_int(canvas, *test, '#000000')

test = 27, 3, 30, 13
dline_Brezen_float(canvas, *test, '#ff0000')

test = 30, 3, 33, 13
dline_CDA(canvas, *test, '#00ff00')
'''

window.mainloop()  # цикл обработки событий
