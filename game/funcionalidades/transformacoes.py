def rotate_point(px, py, cx, cy, angle, math_module):
    rad = math_module.radians(angle)
    x = px - cx
    y = py - cy

    xr = x * math_module.cos(rad) - y * math_module.sin(rad)
    yr = x * math_module.sin(rad) + y * math_module.cos(rad)

    return xr + cx, yr + cy
