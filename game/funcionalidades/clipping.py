INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8


def compute_code(x, y, width, height):
    code = INSIDE
    if x < 0:
        code |= LEFT
    elif x > width:
        code |= RIGHT
    if y < 0:
        code |= TOP
    elif y > height:
        code |= BOTTOM
    return code


def cohen_sutherland(x1, y1, x2, y2, width, height):
    code1 = compute_code(x1, y1, width, height)
    code2 = compute_code(x2, y2, width, height)

    while True:
        if code1 == 0 and code2 == 0:
            return x1, y1, x2, y2
        if code1 & code2:
            return None

        code_out = code1 if code1 else code2

        if code_out & TOP:
            x = x1 + (x2 - x1) * (0 - y1) / (y2 - y1) if y2 != y1 else x1
            y = 0
        elif code_out & BOTTOM:
            x = x1 + (x2 - x1) * (height - y1) / (y2 - y1) if y2 != y1 else x1
            y = height
        elif code_out & RIGHT:
            y = y1 + (y2 - y1) * (width - x1) / (x2 - x1) if x2 != x1 else y1
            x = width
        else:
            y = y1 + (y2 - y1) * (0 - x1) / (x2 - x1) if x2 != x1 else y1
            x = 0

        if code_out == code1:
            x1, y1 = x, y
            code1 = compute_code(x1, y1, width, height)
        else:
            x2, y2 = x, y
            code2 = compute_code(x2, y2, width, height)
