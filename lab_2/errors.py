from tkinter import messagebox

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
    res = "Неправильный ввод коэффициента масштабирования.\nВведите вещественные значения."
    messagebox.showerror("Ошибка", res)

def error_invalid_rotate():
    res = "Неправильный ввод угла поворота.\nВведите вещественное значение (в градусах)."
    messagebox.showerror("Ошибка", res)



def show_task():
    res = ("Задание:  Нарисовать исходный рисунок. Осуществить его перенос, масштабирование и поворот.\n\n\n"
           " ПЕРЕНОС:     ввести в поля x и y кол-во пикселей, на кот. надо сдвинуть изображение.\n\n"
           " МАСШТАБ.:   ввести в поля x и y координаты точки, относительно кот. "
           "будет выполн. масштаб., и коэфф. kx и ky.\n\n"
           " ПОВОРОТ:    ввести в поля x и y координаты точки, относительно кот. "
           "будет выполн. поворот, и угол в градусах. \nПри положительном значении угла поворота\n, "
           "поворот выполняется против часовой стрелки.")
    messagebox.showinfo("Задание", res)
