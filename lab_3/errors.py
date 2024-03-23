from tkinter import messagebox

def error_empty_data():
    res = "Пустой ввод координат x и y."
    messagebox.showerror("Ошибка", res)

def error_invalid_data():
    res = "Неправильный ввод координат.\nВведите целочисленные координаты."
    messagebox.showerror("Ошибка", res)


def error_empty_degree():
    res = "Пустой ввод угла поворота."
    messagebox.showerror("Ошибка", res)

def error_invalid_degree():
    res = "Неправильный ввод угла поворота.\nВведите вещественное число."
    messagebox.showerror("Ошибка", res)


def error_empty_length():
    res = "Пустой ввод радиуса спектра."
    messagebox.showerror("Ошибка", res)

def error_invalid_length():
    res = "Неправильный ввод радиуса спектра.\nВведите целое число."
    messagebox.showerror("Ошибка", res)



def show_task():
    res = ("Задание:  "
           "Примечание: измерение времени работы алгоритмов выполняется по 100 раз.")
    messagebox.showinfo("Задание", res)
