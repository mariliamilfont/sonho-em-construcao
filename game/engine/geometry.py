def rotate_point(px, py, cx, cy, angle, math_module):
    rad = math_module.radians(angle)
    x = px - cx
    y = py - cy

    xr = x * math_module.cos(rad) - y * math_module.sin(rad)
    yr = x * math_module.sin(rad) + y * math_module.cos(rad)

    return xr + cx, yr + cy


def point_in_polygon(x, y, vertices):
    n = len(vertices)
    inside = False

    p1x, p1y = vertices[0]
    for i in range(1, n + 1):
        p2x, p2y = vertices[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def get_polygon_support_y(x, vertices):
    max_y = -float("inf")
    n = len(vertices)

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]

        if min(x1, x2) <= x <= max(x1, x2) and x1 != x2:
            t = (x - x1) / (x2 - x1)
            y = y1 + t * (y2 - y1)
            max_y = max(max_y, y)
        elif x1 == x2 and abs(x - x1) < 1:
            max_y = max(max_y, y1, y2)

    return max_y if max_y != -float("inf") else None


def check_rotated_platform_collision(platform, player_rect, math_module):
    if platform["type"] != "rotate":
        return None

    cx = platform["x"] + platform["w"] / 2
    cy = platform["y"] + platform["h"] / 2

    corners = [
        (platform["x"], platform["y"]),
        (platform["x"] + platform["w"], platform["y"]),
        (platform["x"] + platform["w"], platform["y"] + platform["h"]),
        (platform["x"], platform["y"] + platform["h"]),
    ]

    rotated = [rotate_point(x, y, cx, cy, platform["angle"], math_module) for x, y in corners]

    player_bottom_x = player_rect.centerx
    player_bottom_y = player_rect.bottom

    if point_in_polygon(player_bottom_x, player_bottom_y, rotated):
        support_y = get_polygon_support_y(player_bottom_x, rotated)
        if support_y is not None:
            return support_y

    return None


def rect_circle_collision(rect, cx, cy, r):
    nearest_x = max(rect.left, min(cx, rect.right))
    nearest_y = max(rect.top, min(cy, rect.bottom))
    dx = cx - nearest_x
    dy = cy - nearest_y
    return dx * dx + dy * dy <= r * r
