def set_pixel(draw_surface, width, height, offset_x, offset_y, zoom, x, y, color):
    sx = int((x - offset_x) * zoom)
    sy = int((y - offset_y) * zoom)

    if 0 <= sx < width and 0 <= sy < height:
        draw_surface.set_at((sx, sy), color)
