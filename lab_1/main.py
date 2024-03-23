# Вавилова Варвара ИУ7-44Б
# Нахождение и построение фигуры по заданным координатам

from tkinter import *
from tkinter import ttk
from logic import *
from errors import *

# ARRAY_POINTS = [[-100, -200], [30, 40], [-100, 30], [40, -20], [1000, 1000], [-100, 70]]
# ARRAY_POINTS = [[0, 0], [100, 100], [10, 10], [50, 50], [-100, 70], [-100, -200]]
# ARRAY_POINTS = [[-40, 0], [40, 0], [0, 100]]
# ARRAY_POINTS = [[30, 30]]
ARRAY_POINTS = []

RES_TRIANGLE = [None, None, None]
COUNT_CALCULATIONS = 0
HEIGHT_LENGHT = 0

FONT = 10
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
ZERO_X = CANVAS_WIDTH // 2
ZERO_Y = CANVAS_HEIGHT // 2

window = Tk()  # создаем окошко
window.title("Нахождение и построение фигуры по заданным координатам")
window.geometry('1520x805+0+2')

# CANVAS
canvas = Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="white")
canvas.grid(column=11, row=0, rowspan=12, columnspan=12, sticky=W)


def canvas_update(array):
    if len(ARRAY_POINTS) < 1:
        return
    elif len(ARRAY_POINTS) == 1:
        x, y = ARRAY_POINTS[0]
        k, new_center_x, new_center_y = canvas_scale([[x, y], [-x, -y]])

        if abs(x) < CANVAS_WIDTH / 2 and abs(y) < CANVAS_HEIGHT / 2:
            new_x = ZERO_X + x
            new_y = CANVAS_HEIGHT - ZERO_Y - y
            canvas.create_oval(new_x - 4, new_y - 4, new_x + 4, new_y + 4, fill="red", width=0)
            canvas.create_text(new_x + 5, new_y - 5, text=f'({x:.2f}, {y:.1f})', font=("Arial", FONT), anchor='w')
            return
        else:
            [new_zero_x, new_zero_y] = point_scale(0, 0, new_center_x, new_center_y, k)
            print_grid(new_zero_x, new_zero_y, k)
    else:
        k, new_center_x, new_center_y = canvas_scale(array)
        [new_zero_x, new_zero_y] = point_scale(0, 0, new_center_x, new_center_y, k)
        print_grid(new_zero_x, new_zero_y, k)

    for i in array:
        [x, y] = point_scale(i[0], i[1], new_center_x, new_center_y, k)
        # print("HERE", x, y)
        canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="red", width=0)
        canvas.create_text(x + 5, y - 5, text=f'({i[0]:.2f}, {i[1]:.2f})', font=("Arial", FONT), anchor='w')


def canvas_scale(array):
    min_x = min([point[0] for point in array])
    max_x = max([point[0] for point in array])
    min_y = min([point[1] for point in array])
    max_y = max([point[1] for point in array])

    width = max_x - min_x
    height = max_y - min_y

    new_size = max(width, height)
    k = new_size / (CANVAS_HEIGHT * 0.9)

    new_center_x = width / 2 + min_x
    new_center_y = height / 2 + min_y
    return k, new_center_x, new_center_y


def canvas_del_all():
    canvas.delete("all")
    print_grid(ZERO_X, ZERO_Y, 1)


# POINTS
# _______________________________________________________________________________

def point_scale(x, y, new_center_x, new_center_y, k):
    x = float((x - new_center_x) / k + ZERO_X)
    y = CANVAS_HEIGHT - float((y - new_center_y) / k + ZERO_Y)
    return [x, y]


def point_add():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
        for i in ARRAY_POINTS:
            if [x, y] == i:
                error_point_exist()
                return
        ARRAY_POINTS.append([x, y])
    except ValueError:
        error_invalid_data()


def point_delete():
    try:
        number = int(number_entry.get())
        if number <= 0:
            error_negative_data()
            return
        if number <= len(ARRAY_POINTS):
            ARRAY_POINTS.remove(ARRAY_POINTS[number - 1])
        else:
            error_necessary_point_absense()
    except ValueError:
        error_invalid_point_number()


def point_update():
    try:
        number = int(number_entry.get()) - 1
        if number < 0:
            error_negative_data()
            return
        if number <= len(ARRAY_POINTS):
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
                for i in ARRAY_POINTS:
                    if [x, y] == i:
                        error_point_exist()
                        return
                ARRAY_POINTS[number] = [x, y]
            except ValueError:
                error_invalid_data()
        else:
            error_out_of_range()
    except ValueError:
        error_invalid_point_number()


# _______________________________________________________________________________

def draw_over_side(x_act, y_act, x_cross, y_cross):
    x0, y0, x1, y1, x2, y2 = RES_TRIANGLE[0][0], RES_TRIANGLE[0][1], RES_TRIANGLE[1][0], RES_TRIANGLE[1][1], \
    RES_TRIANGLE[2][0], RES_TRIANGLE[2][1]
    if x_act == x0 and y_act == y0:
        first_point = [x1, y1]
        second_point = [x2, y2]
    elif x_act == x1 and y_act == y1:
        first_point = [x0, y0]
        second_point = [x2, y2]
    else:
        first_point = [x0, y0]
        second_point = [x1, y1]
    first_dist = distance(first_point, [x_cross, y_cross])
    second_dist = distance(second_point, [x_cross, y_cross])
    both_dist = distance(first_point, second_point)
    if abs(both_dist - (first_dist + second_dist)) < EPS:
        return
    if first_dist < second_dist:
        canvas.create_line(first_point[0], first_point[1], x_cross, y_cross, fill="blue", width=3, dash=(10, 5))
    else:
        canvas.create_line(second_point[0], second_point[1], x_cross, y_cross, fill="blue", width=3, dash=(10, 5))


def draw_height(points):
    global HEIGHT_LENGHT
    x_act, y_act, x_cross, y_cross = find_max_height(points)
    HEIGHT_LENGHT = distance([x_act, y_act], [x_cross, y_cross])
    print(x_cross, y_cross)
    x_act_sc, y_act_sc, x_cross_sc, y_cross_sc = find_max_height(RES_TRIANGLE)
    canvas.create_line(x_act_sc, y_act_sc, x_cross_sc, y_cross_sc, fill="red", width=3)  # Из вершины x1, y1
    canvas.create_oval(x_cross_sc - 4, y_cross_sc - 4, x_cross_sc + 4, y_cross_sc + 4, fill="red", width=0)
    canvas.create_text(x_cross_sc + 10, y_cross_sc - 10, text=f'({x_cross:.2f}, {y_cross:.2f})', tags="text",
                       anchor='w', font=("Arial", FONT))
    # print(x_act, y_act, x_cross, y_cross)
    draw_over_side(x_act_sc, y_act_sc, x_cross_sc, y_cross_sc)


def match_3_points(points):
    canvas.create_polygon(*points, fill='', outline='green', width=3)


def result_print():
    if len(ARRAY_POINTS) < 3:
        error_point_absence()
        return
    else:
        global RES_TRIANGLE, COUNT_CALCULATIONS
        RES_TRIANGLE, COUNT_CALCULATIONS = triangle_with_max_height(ARRAY_POINTS)
        if RES_TRIANGLE == None:
            error_result_line()
            return

        x0, y0, x1, y1, x2, y2 = RES_TRIANGLE[0][0], RES_TRIANGLE[0][1], RES_TRIANGLE[1][0], RES_TRIANGLE[1][1], \
            RES_TRIANGLE[2][0], RES_TRIANGLE[2][1]

        res_triangle_tmp = RES_TRIANGLE.copy()
        x_act, y_act, x_cross, y_cross = find_max_height(RES_TRIANGLE)

        k, new_center_x, new_center_y = canvas_scale(RES_TRIANGLE + [[x_cross, y_cross]])
        new_zero_x, new_zero_y = point_scale(0, 0, new_center_x, new_center_y, k)

        print_grid(new_zero_x, new_zero_y, k)

        for i in range(3):
            RES_TRIANGLE[i] = point_scale(RES_TRIANGLE[i][0], RES_TRIANGLE[i][1], new_center_x, new_center_y, k)
            x, y = RES_TRIANGLE[i]
            canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="red", width=0)
            canvas.create_text(x + 5, y - 5, text=f'({res_triangle_tmp[i][0]:.2f}, {res_triangle_tmp[i][1]:.2f})', tags="text",
                               font=("Arial", FONT), anchor='w')

        match_3_points(RES_TRIANGLE)
        draw_height(res_triangle_tmp)
        result_label_draw(x0, y0, x1, y1, x2, y2)
        RES_TRIANGLE = res_triangle_tmp
        canvas.tag_raise("text")


def print_grid(new_zero_x, new_zero_y, k):
    canvas.delete("all")
    if (k > 4):
        return #чтобы сетка не заполняла экран
    step = 20 / k
    for y in range(int(new_zero_y), CANVAS_HEIGHT + 1, int(step)):
        canvas.create_line(0, y, CANVAS_WIDTH, y, fill="black", width=1)
    for y in range(int(new_zero_y), -CANVAS_HEIGHT, -int(step)):
        canvas.create_line(0, y, CANVAS_WIDTH, y, fill="black", width=1)

    for x in range(int(new_zero_x), CANVAS_WIDTH + 1, int(step)):
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill="black", width=1)
    for x in range(int(new_zero_x), -CANVAS_WIDTH, -int(step)):
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill="black", width=1)

    canvas.create_line(new_zero_x, 0, new_zero_x, CANVAS_HEIGHT, fill="black", width=3)
    canvas.create_line(0, new_zero_y, CANVAS_WIDTH, new_zero_y, fill="black", width=3)

    # canvas.create_text(CANVAS_WIDTH - 28, new_zero_y - 13, text="X", font=("Arial", FONT), anchor='w')
    # canvas.create_text(new_zero_x + 5, 30, text="Y", font=("Arial", FONT), anchor='w')


def result_label_draw(x0, y0, x1, y1, x2, y2):
    if COUNT_CALCULATIONS == None or HEIGHT_LENGHT == None:
        return
    count_label.configure(
        text="Количество рассмотренных случаев:    {}\nДлина итоговой высоты:    {:.2f}\n\nВершины треугольника:    \n{}, {}\n{}, {}\n{}, {}".format(
            COUNT_CALCULATIONS, HEIGHT_LENGHT, x0, y0, x1, y1, x2, y2),
        font=("Arial", FONT + 1), anchor=W, justify='left')


# TABLE
# _______________________________________________________________________________
def table_put_all_points():
    for i in range(len(ARRAY_POINTS)):
        table_points.insert("", "end", text=str(i + 1), values=(str(ARRAY_POINTS[i][0]), str(ARRAY_POINTS[i][1])))


def table_del_all():
    table_points.delete(*table_points.get_children())


# _______________________________________________________________________________

def update_all():
    canvas_del_all()
    table_del_all()
    table_put_all_points()
    canvas_update(ARRAY_POINTS)


def result_del_all():
    global HEIGHT_LENGHT, COUNT_CALCULATIONS
    COUNT_CALCULATIONS = 0
    HEIGHT_LENGHT = 0
    result_label_draw("", "", "", "", "", "")


# _______________________________________________________________________

def lock_x_y():
    x_entry.config(state="disabled")
    y_entry.config(state="disabled")
    x_label.config(state="disabled")
    y_label.config(state="disabled")


def unlock_x_y():
    x_entry.config(state="normal")
    y_entry.config(state="normal")
    x_label.config(state="normal")
    y_label.config(state="normal")


def lock_number():
    number_entry.config(state="disabled")
    number_label.config(state="disabled")


def unlock_number():
    number_entry.config(state="normal")
    number_label.config(state="normal")


def unlock_all():
    unlock_number()
    unlock_x_y()


def lock_all():
    lock_x_y()
    lock_number()


def lock_add():
    lock_number()
    unlock_x_y()


def lock_del_update():
    lock_x_y()
    unlock_number()


def choose_radiobutton():
    if VAR.get() == 1:
        point_add()
    elif VAR.get() == 2:
        point_delete()
    elif VAR.get() == 3:
        point_update()
    elif VAR.get() == 4:
        result_print()
        return
    elif VAR.get() == 5:
        result_del_all()
    else:
        canvas_del_all()
        global ARRAY_POINTS
        ARRAY_POINTS = []
        result_del_all()
        table_del_all()
    update_all()


# LABEL
x_label = Label(window, width=10, text=f"x:", font=("Arial", FONT))
y_label = Label(window, width=10, text=f"y:", font=("Arial", FONT))
number_label = Label(window, width=12, text=f"Точка номер:", font=("Arial", FONT))
count_label = Label(window,
                    text=f"Количество рассмотренных случаев:\nДлина итоговой высоты:\n\nВершины треугольника:\n",
                    font=("Arial", FONT + 1), anchor=W, justify='left')
empty_label = Label(window, width=20, text=f" ")
x_label.grid(column=0, row=0, sticky=W)
y_label.grid(column=0, row=1, sticky=W)
number_label.grid(column=7, row=0, rowspan=2, sticky=W)
empty_label.grid(column=9, row=0, rowspan=12, sticky=W)
count_label.grid(column=1, row=6, rowspan=3, columnspan=7, sticky=W)

# ENTRY
x_entry = Entry(window, width=33)
y_entry = Entry(window, width=33)
number_entry = Entry(window, width=5)
x_entry.grid(column=1, row=0, columnspan=4, sticky=W)
y_entry.grid(column=1, row=1, columnspan=4, sticky=W)
number_entry.grid(column=8, row=0, rowspan=2, sticky=E)

# BUTTON
butt_output = Button(window, width=30, height=1, text="Запуск", command=choose_radiobutton, font=("Arial", FONT + 2))
butt_output.grid(column=1, row=5, columnspan=4, sticky=EW)
butt_task = Button(window, width=15, height=3, text="Показать\nзадание", command=show_task, font=("Arial", FONT + 3))
butt_task.grid(column=7, row=6, columnspan=3, rowspan=4)

# RADIOBUTTON
VAR = IntVar()
VAR.set(1)
rb_point_add = Radiobutton(window, text="Добавить точку", variable=VAR, value=1, command=lock_add, font=("Arial", FONT))
rb_point_del = Radiobutton(window, text="Удалить точку", variable=VAR, value=2, command=lock_del_update,
                           font=("Arial", FONT))
rb_point_edit = Radiobutton(window, text="Изменить точку", variable=VAR, value=3, command=unlock_all,
                            font=("Arial", FONT))
rb_res = Radiobutton(window, text="Результат", variable=VAR, value=4, command=lock_all, font=("Arial", FONT))
rb_del_res = Radiobutton(window, text="Удалить результат", variable=VAR, value=5, command=lock_all,
                         font=("Arial", FONT))
rb_del_all = Radiobutton(window, text="Удалить всё", variable=VAR, value=6, command=lock_all, font=("Arial", FONT))
rb_point_add.grid(column=1, row=2, columnspan=3, sticky=W, pady=1)
rb_point_del.grid(column=1, row=3, columnspan=3, sticky=W, pady=1)
rb_point_edit.grid(column=1, row=4, columnspan=2, sticky=W, pady=1)
rb_res.grid(column=7, row=2, columnspan=3, sticky=W, pady=1)
rb_del_res.grid(column=7, row=3, columnspan=3, sticky=W, pady=1)
rb_del_all.grid(column=7, row=4, columnspan=2, sticky=W, pady=1)

# TABLE
table_points = ttk.Treeview(window, columns=('first_coordinate', 'second_coordinate'))
table_points["columns"] = ("first_coordinate", "second_coordinate")
table_points.column("#0", width=40)
table_points.column("first_coordinate", width=100)
table_points.column("second_coordinate", width=100)
table_points.heading('#0', text='№')
table_points.heading('first_coordinate', text='x')
table_points.heading('second_coordinate', text='y')
table_points.grid(column=1, row=10, columnspan=8, rowspan=4, sticky=NSEW)

# _______________________________________________________________________
update_all()
lock_number()
unlock_x_y()
result_label_draw("", "", "", "", "", "")
# _______________________________________________________________________


window.mainloop()  # цикл обработки событий
