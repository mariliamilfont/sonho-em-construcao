def draw_line(x0, y0, x1, y1, color, set_pixel_fn, cohen_sutherland_fn):
    clipped = cohen_sutherland_fn(x0, y0, x1, y1)
    if clipped is None:
        return

    x0, y0, x1, y1 = clipped
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        set_pixel_fn(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def draw_circle(cx, cy, r, color, set_pixel_fn):
    x = 0
    y = r
    d = 1 - r

    while x <= y:
        points = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x),
        ]
        for px, py in points:
            set_pixel_fn(px, py, color)

        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1


def draw_ellipse(cx, cy, rx, ry, color, set_pixel_fn):
    for x in range(-rx, rx):
        y = int((1 - (x * x) / (rx * rx)) ** 0.5 * ry)
        set_pixel_fn(cx + x, cy + y, color)
        set_pixel_fn(cx + x, cy - y, color)


def draw_filled_circle(cx, cy, r, color, draw_line_fn):
    for dy in range(-r, r + 1):
        dx = int((r * r - dy * dy) ** 0.5)
        draw_line_fn(cx - dx, cy + dy, cx + dx, cy + dy, color)
