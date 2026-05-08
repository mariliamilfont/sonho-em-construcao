import math


def fill_polygon_scanline(vertices, color, width, height, set_pixel_fn):
    if len(vertices) < 3:
        return

    min_y = max(0, math.ceil(min(v[1] for v in vertices)))
    max_y = min(height - 1, math.floor(max(v[1] for v in vertices)))

    for y in range(min_y, max_y + 1):
        intersections = []
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]

            if y1 == y2:
                continue

            if min(y1, y2) <= y < max(y1, y2):
                t = (y - y1) / (y2 - y1)
                x = x1 + t * (x2 - x1)
                intersections.append(x)

        intersections.sort()
        for i in range(0, len(intersections) - 1, 2):
            x_start = max(0, math.ceil(intersections[i]))
            x_end = min(width - 1, math.floor(intersections[i + 1]))
            for x in range(x_start, x_end + 1):
                set_pixel_fn(x, y, color)


def fill_polygon_gradient_scanline(vertices, colors, width, height, set_pixel_fn):
    if len(vertices) < 3 or len(vertices) != len(colors):
        return

    min_y = max(0, math.ceil(min(v[1] for v in vertices)))
    max_y = min(height - 1, math.floor(max(v[1] for v in vertices)))

    for y in range(min_y, max_y + 1):
        intersections = []
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            c1 = colors[i]
            c2 = colors[(i + 1) % len(vertices)]

            if y1 == y2:
                continue

            if min(y1, y2) <= y < max(y1, y2):
                t = (y - y1) / (y2 - y1)
                x = x1 + t * (x2 - x1)
                r = c1[0] + t * (c2[0] - c1[0])
                g = c1[1] + t * (c2[1] - c1[1])
                b = c1[2] + t * (c2[2] - c1[2])
                intersections.append((x, r, g, b))

        intersections.sort(key=lambda item: item[0])
        for i in range(0, len(intersections) - 1, 2):
            x1, r1, g1, b1 = intersections[i]
            x2, r2, g2, b2 = intersections[i + 1]

            xs = max(0, math.ceil(x1))
            xe = min(width - 1, math.floor(x2))
            span = x2 - x1

            for x in range(xs, xe + 1):
                t = 0 if span == 0 else (x - x1) / span
                r = int(r1 + t * (r2 - r1))
                g = int(g1 + t * (g2 - g1))
                b = int(b1 + t * (b2 - b1))
                set_pixel_fn(x, y, (r, g, b))


def fill_polygon_texture_scanline(
    vertices,
    tex_coords,
    width,
    height,
    set_pixel_fn,
    texture_cache,
    texture_w,
    texture_h,
):
    if len(vertices) < 3 or len(vertices) != len(tex_coords):
        return

    min_y = max(0, math.ceil(min(v[1] for v in vertices)))
    max_y = min(height - 1, math.floor(max(v[1] for v in vertices)))

    for y in range(min_y, max_y + 1):
        intersections = []
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            u1, v1 = tex_coords[i]
            u2, v2 = tex_coords[(i + 1) % len(vertices)]

            if y1 == y2:
                continue

            if min(y1, y2) <= y < max(y1, y2):
                t = (y - y1) / (y2 - y1)
                x = x1 + t * (x2 - x1)
                u = u1 + t * (u2 - u1)
                v = v1 + t * (v2 - v1)
                intersections.append((x, u, v))

        intersections.sort(key=lambda item: item[0])
        for i in range(0, len(intersections) - 1, 2):
            x1, u1, v1 = intersections[i]
            x2, u2, v2 = intersections[i + 1]

            xs = max(0, math.ceil(x1))
            xe = min(width - 1, math.floor(x2))
            span = x2 - x1

            for x in range(xs, xe + 1):
                t = 0 if span == 0 else (x - x1) / span
                u = int(u1 + t * (u2 - u1)) % texture_w
                v = int(v1 + t * (v2 - v1)) % texture_h
                set_pixel_fn(x, y, texture_cache[u][v])


def flood_fill(x, y, target_color, new_color, width, height, draw_surface, set_pixel_fn):
    if target_color == new_color:
        return

    stack = [(x, y)]
    visited = set()

    while stack:
        px, py = stack.pop()
        key = (px, py)

        if key in visited:
            continue
        visited.add(key)

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if draw_surface.get_at((px, py))[:3] != target_color:
            continue

        set_pixel_fn(px, py, new_color)

        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))
