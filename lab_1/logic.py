import math as m
# import itertools

EPS = 1e-10


def distance(p1, p2):
    return m.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def is_strength(min_side, first_other, second_other, x, y, x_side_1, y_side_1, x_side_2, y_side_2):
    if first_other < second_other:
        if abs(second_other ** 2 - (first_other ** 2 + min_side ** 2)) < EPS:
            return True, x, y, x_side_2, y_side_2
        return False, 0, 0, 0, 0
    elif first_other > second_other:
        if abs(first_other ** 2 - (second_other ** 2 + min_side ** 2)) < EPS:
            return True, x, y, x_side_1, y_side_1
        return False, 0, 0, 0, 0
    else:
        return False, 0, 0, 0, 0


def count_k_line(x1, y1, x2, y2):
    k = (y1 - y2) / (x1 - x2)
    return k

def count_b_line(x, y, k):
    b = y - k * x
    return b

def count_x_line(b1, k1, b2, k2):
    x = (b2 - b1) / (k1 - k2)
    return x




def find_max_height(points):
    x0, y0, x1, y1, x2, y2 = points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1]

    first_side = distance(points[1], points[2])
    second_side = distance(points[0], points[2])
    third_side = distance(points[0], points[1])
    min_side = min(first_side, second_side, third_side)

    if min_side == first_side:
        first_other, second_other = second_side, third_side
        x_side_1, y_side_1 = x1, y1
        x_side_2, y_side_2 = x2, y2
        x_act, y_act = x0, y0
    elif min_side == second_side:
        first_other, second_other = first_side, third_side
        x_side_1, y_side_1 = x0, y0
        x_side_2, y_side_2 = x2, y2
        x_act, y_act = x1, y1
    else:
        first_other, second_other = first_side, second_side
        x_side_1, y_side_1 = x0, y0
        x_side_2, y_side_2 = x1, y1
        x_act, y_act = x2, y2

    res, x, y, x_end, y_end = is_strength(min_side, first_other, second_other, x_act, y_act, x_side_1, y_side_1,
                                          x_side_2, y_side_2)
    if res:
        return x, y, x_end, y_end

    if x_side_1 == x_side_2:
        x_cross = x_side_1
        y_cross = y_act

    elif y_side_1 == y_side_2:
        y_cross = y_side_1
        x_cross = x_act
    else:
        k1 = count_k_line(x_side_1, y_side_1, x_side_2, y_side_2)
        k2 = 0 if k1 == 0 else -1 / k1
        b1 = count_b_line(x_side_1, y_side_1, k1)
        b2 = count_b_line(x_act, y_act, k2)
        x_cross = count_x_line(b1, k1, b2, k2)
        y_cross = k2 * x_cross + b2

    return x_act, y_act, x_cross, y_cross


def triangle_with_max_height(arr_point):
    res_height_max = 0
    result_triangle = None
    count_calculations = 0

    for a in range(len(arr_point) - 2):
        for b in range(a + 1, len(arr_point) - 1):
            for c in range(b + 1, len(arr_point)):
                count_calculations += 1
                x_act, y_act, x_cross, y_cross = find_max_height([arr_point[a], arr_point[b], arr_point[c]])
                height_max = distance([x_act, y_act], [x_cross, y_cross])
                if height_max > res_height_max and height_max > 0:
                    res_height_max = height_max
                    result_triangle = [arr_point[a], arr_point[b], arr_point[c]]


    return result_triangle, count_calculations
