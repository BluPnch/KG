# Вавилова Варвара ИУ7-44Б
# Перенос, масштабирование и поворот рисунка

from tkinter import *
from copy import deepcopy
from tkinter import ttk
from tkinter import messagebox
from logic import *

OVAL_INFO = [[11.5, 3.25], 1.25]
OVAL_POINTS = []

ARRAY_POINTS = [[[0, 0], [17, 0]],  # земля

                [[3, 0], [3, 6]],  # стены
                [[14, 6], [14, 0]],
                [[2, 6], [3, 9]],  # крыша
                [[3, 9], [14, 9]],
                [[14, 9], [15, 6]],
                [[2, 6], [15, 6]],

                [[4.5, 0], [4.5, 5]],  # дверь
                [[4.5, 5], [7.5, 5]],
                [[7.5, 5], [7.5, 0]],
                [[4.5, 5], [7.5, 0]],
                [[4.5, 0], [7.5, 5]],

                [[6.75, 2], [6.75, 3]],  # ручка
                [[7.25, 2], [7.25, 3]],
                [[6.75, 2], [7.25, 2]],
                [[7.25, 3], [6.75, 3]],

                [[11.5, 2], [11.5, 4.5]],  # окно
                [[10.25, 3.25], [12.75, 3.25]]]

POINT_SCALE = [0, 0]

CANVAS_LENGTH = 800
POINTS_IN_CELL = 18
P_TO_MOVE = 15
CENTER_POINT = [8.5, 4.5]
FONT = 14

HISTORY = [[ARRAY_POINTS, OVAL_POINTS, CENTER_POINT]]
# ARRAY_POINTS, OVAL_POINTS, CENTER_POINT



window = Tk()  # создаем окошко
window.title("Перенос, масштабирование и поворот рисунка")
# window.geometry('1500x800+15+10')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")
# window.attributes('-fullscreen', True)

# CANVAS
canvas_original = Canvas(window, width=CANVAS_LENGTH, height=CANVAS_LENGTH, background="white")
canvas_original.grid(column=7, row=0, columnspan=20, rowspan=20, sticky=NSEW)


def center_picture():
    for line in ARRAY_POINTS:
        p_1 = line[0]
        p_2 = line[1]
        p_1[0], p_1[1], p_2[0], p_2[1] = map(lambda x: (x + P_TO_MOVE) * POINTS_IN_CELL,
                                             [p_1[0], p_1[1], p_2[0], p_2[1]])

    get_oval_points(OVAL_INFO[0][0], OVAL_INFO[0][1], OVAL_INFO[1])
    for i in range(len(OVAL_POINTS)):
        x, y = OVAL_POINTS[i]
        OVAL_POINTS[i] = list(map(lambda x: (x + P_TO_MOVE) * POINTS_IN_CELL, [x, y]))
    CENTER_POINT[0], CENTER_POINT[1] = map(
        lambda x: (x + P_TO_MOVE) * POINTS_IN_CELL, [CENTER_POINT[0], CENTER_POINT[1]])



def get_oval_points(x_center, y_center, radius):
    global OVAL_POINTS
    num_points = 100
    step = 360 / num_points
    for i in range(num_points):
        alpha = m.radians(i * step)
        x = x_center + radius * m.cos(alpha)
        y = y_center + radius * m.sin(alpha)
        OVAL_POINTS.append([x, y])


# PICTURE CHANGE
# __________________________________________________________________________________

def picture_draw():
    canvas_original.delete("all")
    for [[start_x, start_y], [end_x, end_y]] in ARRAY_POINTS:
        canvas_original.create_line(start_x, CANVAS_LENGTH - start_y, end_x, CANVAS_LENGTH - end_y, fill="black",
                                    width=3)
    tmp_oval_points = deepcopy(OVAL_POINTS)
    for i in range(len(tmp_oval_points)):
        tmp_oval_points[i][1] = CANVAS_LENGTH - tmp_oval_points[i][1]
    canvas_original.create_polygon(tmp_oval_points, outline="black", fill="", width=3)
    x, y = CENTER_POINT[0], CANVAS_LENGTH - CENTER_POINT[1]
    canvas_original.create_oval(x - 4, y - 4, x + 4, y + 4, fill="red", width=0)
    center_res_label.configure(
        text=f'({CENTER_POINT[0]:.2f}, {CENTER_POINT[1]:.2f})', font=("Tahoma", FONT), anchor=W,
        justify='left')


def picture_transf(x, y):
    global HISTORY
    HISTORY.append([deepcopy(ARRAY_POINTS), deepcopy(OVAL_POINTS), deepcopy(CENTER_POINT)])
    for i in range(len(ARRAY_POINTS)):
        [[start_x, start_y], [end_x, end_y]] = ARRAY_POINTS[i]
        ARRAY_POINTS[i][0] = [start_x + x, start_y + y]
        ARRAY_POINTS[i][1] = [end_x + x, end_y + y]
    for i in range(len(OVAL_POINTS)):
        x_p, y_p = OVAL_POINTS[i]
        OVAL_POINTS[i] = [x_p + x, y_p + y]
    CENTER_POINT[0] += x
    CENTER_POINT[1] += y


def picture_zoom(x, y, kx, ky):
    global HISTORY
    HISTORY.append([deepcopy(ARRAY_POINTS), deepcopy(OVAL_POINTS), deepcopy(CENTER_POINT)])
    for i in range(len(ARRAY_POINTS)):
        [[start_x, start_y], [end_x, end_y]] = ARRAY_POINTS[i]
        ARRAY_POINTS[i][0] = point_scale(start_x, start_y, x, y, kx, ky)
        ARRAY_POINTS[i][1] = point_scale(end_x, end_y, x, y, kx, ky)
    for i in range(len(OVAL_POINTS)):
        x_p, y_p = OVAL_POINTS[i]
        OVAL_POINTS[i] = point_scale(x_p, y_p, x, y, kx, ky)
    CENTER_POINT[0], CENTER_POINT[1] = point_scale(CENTER_POINT[0], CENTER_POINT[1], x, y, kx, ky)


def picture_rotation(rot_x, rot_y, psi):
    global HISTORY
    HISTORY.append([deepcopy(ARRAY_POINTS), deepcopy(OVAL_POINTS), deepcopy(CENTER_POINT)])
    for i in range(len(ARRAY_POINTS)):
        [[start_x, start_y], [end_x, end_y]] = ARRAY_POINTS[i]
        ARRAY_POINTS[i][0][0], ARRAY_POINTS[i][0][1] = point_rotate(start_x, start_y, rot_x, rot_y, psi)
        ARRAY_POINTS[i][1][0], ARRAY_POINTS[i][1][1] = point_rotate(end_x, end_y, rot_x, rot_y, psi)
    for i in range(len(OVAL_POINTS)):
        x_p, y_p = OVAL_POINTS[i]
        OVAL_POINTS[i] = point_rotate(x_p, y_p, rot_x, rot_y, psi)
    CENTER_POINT[0], CENTER_POINT[1] = point_rotate(CENTER_POINT[0], CENTER_POINT[1], rot_x, rot_y, psi)




# _______________________________________________________________________
def transfer():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
        picture_transf(x, y)
        picture_draw()
        table_history.insert("", "end", text=str(len(HISTORY) - 1),
                             values=("Перенос", str(x), str(y), "-", "-", "-"))
    except ValueError:
        if x_entry.get() == "" or y_entry.get() == "":
            error_empty_data()
        else:
            error_invalid_data()


def zoom():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
        try:
            kx = float(kx_entry.get())
            ky = float(ky_entry.get())

            picture_zoom(x, y, kx, ky)
            picture_draw()
            canvas_original.create_oval(x - 4, CANVAS_LENGTH - y - 4, x + 4, CANVAS_LENGTH - y + 4, fill="blue",
                                        width=0)
            canvas_original.create_text(x + 5, CANVAS_LENGTH - y - 5, text=f'({x:.2f}, {y:.2f})',
                                        tags="text", font=("Tahoma", FONT))
            table_history.insert("", "end", text=str(len(HISTORY) - 1),
                                 values=("Маштабирование", str(x), str(y), str(kx), str(ky), "-"))
        except ValueError:
            error_invalid_zoom()
    except ValueError:
        if x_entry.get() == "" or y_entry.get() == "":
            error_empty_data()
        else:
            error_invalid_data()


def rotate():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
        try:
            psi = float(degree_entry.get())
            picture_rotation(x, y, psi)
            picture_draw()
            canvas_original.create_oval(x - 4, CANVAS_LENGTH - y - 4, x + 4, CANVAS_LENGTH - y + 4, fill="blue",
                                        width=0)
            canvas_original.create_text(x + 5, CANVAS_LENGTH - y - 5, text=f'({x:.2f}, {y:.2f})',
                                        tags="text", font=("Tahoma", FONT))

            table_history.insert("", "end", text=str(len(HISTORY) - 1),
                                 values=("Поворот", str(x), str(y), "-", "-", str(psi)))
        except ValueError:
            error_invalid_rotate()
    except ValueError:
        if x_entry.get() == "" or y_entry.get() == "":
            error_empty_data()
        else:
            error_invalid_data()


def picture_original():
    global HISTORY, ARRAY_POINTS, OVAL_POINTS, CENTER_POINT
    ARRAY_POINTS, OVAL_POINTS, CENTER_POINT = deepcopy(HISTORY[0][0]), deepcopy(HISTORY[0][1]), deepcopy(HISTORY[0][2])
    picture_draw()
    HISTORY.append([deepcopy(ARRAY_POINTS), deepcopy(OVAL_POINTS), deepcopy(CENTER_POINT)])
    table_history.insert("", "end", text=str(len(HISTORY) - 1), values=("Начальное изображение", "-", "-", "-", "-", "-"))


def rollback():
    global HISTORY, ARRAY_POINTS, OVAL_POINTS, CENTER_POINT

    if len(HISTORY) <= 1:
        error_invalid_rollback()
        return

    n = len(HISTORY) - 1
    ARRAY_POINTS, OVAL_POINTS, CENTER_POINT = deepcopy(HISTORY[n][0]), deepcopy(HISTORY[n][1]), deepcopy(HISTORY[n][2])
    picture_draw()
    HISTORY.pop()
    last_item_id = table_history.get_children()[-1]
    table_history.delete(last_item_id)

# _______________________________________________________________________

def error_invalid_rollback():
    res = "Невозможно сделать откат. История пуста."
    messagebox.showerror("Ошибка", res)

def error_empty_data():
    res = "Пустой ввод координат x и y."
    messagebox.showerror("Ошибка", res)

def error_invalid_data():
    res = "Неправильный ввод координат.\nВведите вещественные координаты."
    messagebox.showerror("Ошибка", res)

def error_invalid_zoom():
    res = "Неправильный ввод коэффициента масштабирования.\nВведите вещественные координаты."
    messagebox.showerror("Ошибка", res)

def error_invalid_rotate():
    res = "Неправильный ввод угла поворота.\nВведите вещественное значение (в градусах)."
    messagebox.showerror("Ошибка", res)



def show_task():
    res = ("Задание:  Нарисовать исходный рисунок. Осуществить его перенос, масштабирование и поворот.\n\n\nПримечания"
           " ПЕРЕНОС:     ввести в поля x и y кол-во пикселей, на кот. надо сдвинуть изображение.\n\n"
           " МАСШТАБ.:   ввести в поля x и y координаты точки, относительно кот. "
           "будет выполн. масштаб., и коэфф. kx и ky.\n\n"
           " ПОВОРОТ:    ввести в поля x и y координаты точки, относительно кот. "
           "будет выполн. поворот, и угол в градусах.")
    messagebox.showinfo("Задание", res)

center_picture()
picture_draw()

# _______________________________________________________________________
# BUTTON
butt_transfer = Button(window, width=15, text="Перенос", command=transfer, font=("Tahoma", FONT - 1))
butt_transfer.grid(column=3, row=1, columnspan=2, sticky=EW)
butt_zoom = Button(window, width=15, text="Масштабирование", command=zoom, font=("Tahoma", FONT - 1))
butt_zoom.grid(column=3, row=2, columnspan=2, sticky=EW)
butt_rotation = Button(window, width=15, text="Повернуть", command=rotate, font=("Tahoma", FONT - 1))
butt_rotation.grid(column=3, row=5, columnspan=2, sticky=EW)
butt_task = Button(window, width=15, height=3, text="Откат\nна 1 шаг", command=rollback, font=("Tahoma", FONT - 1))
butt_task.grid(column=0, row=8, columnspan=1, rowspan=2, sticky=NS)
butt_task = Button(window, width=20, height=3, text="Исходное\nизображение", command=picture_original, font=("Tahoma", FONT - 1))
butt_task.grid(column=1, row=8, columnspan=2, rowspan=2, sticky=NS)
butt_task = Button(window, width=15, height=3, text="Показать\nзадание", command=show_task, font=("Tahoma", FONT - 1))
butt_task.grid(column=3, row=8, columnspan=1, rowspan=2, sticky=NS)

# ENTRY
x_entry = Entry(window, width=15, font=("Tahoma", FONT))
y_entry = Entry(window, width=15, font=("Tahoma", FONT))
kx_entry = Entry(window, width=15, font=("Tahoma", FONT))
ky_entry = Entry(window, width=15, font=("Tahoma", FONT))
degree_entry = Entry(window, width=15, font=("Tahoma", FONT))

x_entry.grid(column=1, row=1, sticky=W)
y_entry.grid(column=1, row=2, sticky=W)
kx_entry.grid(column=1, row=3, sticky=W)
ky_entry.grid(column=3, row=3, sticky=W)
degree_entry.grid(column=1, row=5, sticky=W)

x_entry.insert(END, "423")
y_entry.insert(END, "351")
kx_entry.insert(END, "1")
ky_entry.insert(END, "1")
degree_entry.insert(END, "0")

# LABEL
transfer_zoom_label = Label(window, text=f"Перенос/Масштабирование", font=("Tahoma", FONT + 1), anchor="center",
                            justify='left')
x_label = Label(window, width=15, text=f"x:", font=("Tahoma", FONT), anchor="center", justify='left')
y_label = Label(window, width=15, text=f"y:", font=("Tahoma", FONT), anchor="center", justify='left')
kx_label = Label(window, width=15, text=f"Коэфф. x:", font=("Tahoma", FONT), anchor="center", justify='left')
ky_label = Label(window, width=15, text=f"Коэфф. y:", font=("Tahoma", FONT), anchor="center", justify='left')
rotation_label = Label(window, text=f"Поворот", font=("Tahoma", FONT + 1), anchor="center", justify='left')
degree_label = Label(window, width=15, text=f"Градусы:", font=("Tahoma", FONT), anchor="center", justify='left')
center_point_label = Label(window, width=40, text=f"Координаты центра рисунка: ", font=("Tahoma", FONT), anchor=W,
                           justify='left')
center_res_label = Label(window, width=15, text="({}, {})".format(CENTER_POINT[0], CANVAS_LENGTH - CENTER_POINT[0]),
                         font=("Tahoma", FONT), anchor=W,
                         justify='left')
empty_horiz_1 = Label(window, width=3, text=f" ", font=("Tahoma", FONT))
empty_horiz_2 = Label(window, width=3, text=f" ", font=("Tahoma", FONT))
empty_vertic = Label(window, width=7, text=f" ", font=("Tahoma", FONT))

# _____GRID_____
transfer_zoom_label.grid(column=1, row=0, columnspan=2, sticky=W)
x_label.grid(column=0, row=1, sticky=W)
y_label.grid(column=0, row=2, sticky=W)
kx_label.grid(column=0, row=3, sticky=W)
ky_label.grid(column=2, row=3, sticky=W)
rotation_label.grid(column=1, row=4, sticky=W)
degree_label.grid(column=0, row=5, sticky=W)
center_point_label.grid(column=1, row=6, columnspan=3, sticky=W)
center_res_label.grid(column=3, row=6, columnspan=2, sticky=W)

empty_horiz_1.grid(column=0, row=7, columnspan=5, sticky=EW)
empty_horiz_2.grid(column=0, row=10, columnspan=5, sticky=EW)

empty_vertic.grid(column=5, row=0, rowspan=14, columnspan=2, sticky=EW)

# _______________________________________________________________________
# TABLE
table_history = ttk.Treeview(window, columns=('action', 'x', 'y', 'kx', 'ky', 'psi'))
table_history["columns"] = ('action', 'x', 'y', 'kx', 'ky', 'psi')
table_history.column("#0", width=30)
table_history.column("action", width=100)
table_history.column("x", width=50)
table_history.column("y", width=50)
table_history.column("kx", width=50)
table_history.column("ky", width=50)
table_history.column("psi", width=50)

table_history.heading('#0', text='№')
table_history.heading('action', text='Действие')
table_history.heading('x', text='x')
table_history.heading('y', text='y')
table_history.heading('kx', text='kx')
table_history.heading('ky', text='ky')
table_history.heading('psi', text='psi')
table_history.grid(column=0, row=11, columnspan=4, rowspan=10, sticky=NSEW)

# table_history.tag_configure('bold', font=("Tahoma", FONT, "bold"))
# for col in table_history["columns"]:
#     table_history.heading(col, text=col.title(), anchor=W)


window.mainloop()  # цикл обработки событий

ef task_1():
    x_input = float(input("Введите число x: "))
    #
    # print("\n____________________________________________________________________________")
    # print("NEWTON\n")
    #
    x_arr, y0_arr, y1_arr, y2_arr = clean_arrays()
    file_open("lab_hermit.txt", x_arr, y0_arr, y1_arr, y2_arr, "hermit")
    # print("{:<4} {:<10} {:<10}".format("", "X", "Y"))
    # newt_table_print(x_arr, y0_arr)
    # y_newt = newt(x_arr, y0_arr, x_input, n_input)
    # print()
    #
    # print("\n____________________________________________________________________________")
    # print("HERMIT\n")
    #
    # x_arr, y0_arr, y1_arr, y2_arr = clean_arrays()
    # file_open("lab_hermit.txt", x_arr, y0_arr, y1_arr, y2_arr, "hermit")
    table_print(x_arr, y0_arr, y1_arr, y2_arr)
    # y_hermit = hermit(x_arr, y0_arr, y1_arr, y2_arr, x_input, n_input)
    #
    # print("Результат по полиному Ньютона: ", x_input, y_newt)
    # print("Результат по полиному Эрмита: ", x_input, y_hermit)

    table_different_n(x_arr, y0_arr, y1_arr, y2_arr, x_input)
