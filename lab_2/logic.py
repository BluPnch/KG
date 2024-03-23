import math as m

# POINT CHANGE
# __________________________________________________________________________________

def point_scale(x, y, zoom_x, zoom_y, kx, ky):
    x = (x - zoom_x) * kx + zoom_x
    y = (y - zoom_y) * ky + zoom_y
    return [x, y]


def point_rotate(x, y, rotate_x, rotate_y, psi_degree):
    psi_rad = m.radians(psi_degree)
    new_x = rotate_x + (x - rotate_x) * m.cos(psi_rad) - (y - rotate_y) * m.sin(psi_rad)
    new_y = rotate_y + (y - rotate_y) * m.cos(psi_rad) + (x - rotate_x) * m.sin(psi_rad)
    return [new_x, new_y]