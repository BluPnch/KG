from tkinter import messagebox

FONT_MESS = 14

# TASK
# ____________________________________________________________________________
def show_task():
    res = "На плоскости дано множество точек.\n" \
          "Найти такой треугольник с вершинами в этих точках, у которого высота имеет максмальную длину.\n" \
          "(Для каждого треугольник беретсята из трех высот, длина которой максимальна)."
    messagebox.showinfo("Задание", res)


# ERRORS
# ____________________________________________________________________________

def error_invalid_point_number():
    res = "Неправильно введенные данные.\nВведите натуральное значение."
    messagebox.showerror("Ошибка", res)


def error_point_exist():
    res = "Такая точка уже есть."
    messagebox.showerror("Ошибка", res)


def error_result_line():
    res = "Вырожденный случай.\nДобавьте еще одну или несколько точек для получения результата."
    messagebox.showerror("Ошибка", res)


def error_out_of_range():
    res = "Такого номера точки нет.\nПовторите попытку."
    messagebox.showerror("Ошибка", res)


def error_invalid_data():
    res = "Неправильно введенные данные.\nВведите вещественные координаты."
    messagebox.showerror("Ошибка", res)


def error_necessary_point_absense():
    res = "Такой точки нет в списке."
    messagebox.showerror("Ошибка", res)


def error_point_absence():
    res = "Нет достаточного количества точек."
    messagebox.showerror("Ошибка", res)


def error_negative_data():
    res = "Необходимо ввести неотрицательное число."
    messagebox.showerror("Ошибка", res)
