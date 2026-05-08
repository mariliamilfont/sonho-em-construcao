def draw_textured_rect(x, y, w, h, fill_polygon_texture_scanline_fn):
    vertices = [
        (x, y),
        (x + w, y),
        (x + w, y + h),
        (x, y + h),
    ]
    tex_coords = [
        (0, 0),
        (w, 0),
        (w, h),
        (0, h),
    ]
    fill_polygon_texture_scanline_fn(vertices, tex_coords)


def fill_textured_background(width, height, tex_cache, tex_w, tex_h, set_pixel_fn):
    for y in range(height):
        for x in range(width):
            tx = x % tex_w
            ty = y % tex_h
            set_pixel_fn(x, y, tex_cache[tx][ty])
