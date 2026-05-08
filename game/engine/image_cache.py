def surface_to_cache(surface):
    w, h = surface.get_width(), surface.get_height()
    return [[surface.get_at((x, y)) for y in range(h)] for x in range(w)]


def resize_cache_nearest(src_cache, src_w, src_h, dst_w, dst_h):
    if src_w <= 0 or src_h <= 0:
        return [[(255, 255, 255, 255) for _ in range(dst_h)] for _ in range(dst_w)]

    dst_cache = [[None for _ in range(dst_h)] for _ in range(dst_w)]
    for x in range(dst_w):
        src_x = int(x * src_w / dst_w)
        if src_x >= src_w:
            src_x = src_w - 1
        for y in range(dst_h):
            src_y = int(y * src_h / dst_h)
            if src_y >= src_h:
                src_y = src_h - 1
            dst_cache[x][y] = src_cache[src_x][src_y]
    return dst_cache
