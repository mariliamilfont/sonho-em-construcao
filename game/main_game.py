import pygame
import sys
import math
from collections import defaultdict

pygame.init()

# ================== JANELA E VIEWPORT ==================
# Coordenadas de Dispositivo (Tela): 800x600 pixels
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sonhos em Construção")

clock = pygame.time.Clock()

# Surface alvo para rasterizacao por pixel.
draw_surface = screen

# ================== TRANSFORMAÇÃO DE COORDENADAS ==================
# Transforma coordenadas de MUNDO para coordenadas de DISPOSITIVO (tela)
# Fórmula: x_dispositivo = (x_mundo - offset_x) * zoom
#          y_dispositivo = (y_mundo - offset_y) * zoom
# 
# offset_x, offset_y: translação (pan)
# zoom: escala (zoom in/out)
# 
# VIEWPORT: define a área visível da tela onde os pixels são renderizados
# VIEWPORT atual: [0, 0] a [WIDTH, HEIGHT]

zoom = 1.0          # Escala/zoom (padrão 1.0 = sem zoom)
offset_x = 0        # Translação X (mundo → dispositivo)
offset_y = 0        # Translação Y (mundo → dispositivo)


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

# ================== TEXTURA ==================
texture = pygame.image.load("assets/images/plataforma.png")
texture_src_w, texture_src_h = texture.get_width(), texture.get_height()
texture_src_cache = surface_to_cache(texture)
texture_w, texture_h = 50, 50
texture_cache = resize_cache_nearest(
    texture_src_cache,
    texture_src_w,
    texture_src_h,
    texture_w,
    texture_h,
)

texture2 = pygame.image.load("assets/images/plataforma2.png")
texture2_src_w, texture2_src_h = texture2.get_width(), texture2.get_height()
texture2_src_cache = surface_to_cache(texture2)
texture2_w, texture2_h = 50, 50
texture2_cache = resize_cache_nearest(
    texture2_src_cache,
    texture2_src_w,
    texture2_src_h,
    texture2_w,
    texture2_h,
)

texture3 = pygame.image.load("assets/images/plataforma3.png")
texture3_src_w, texture3_src_h = texture3.get_width(), texture3.get_height()
texture3_src_cache = surface_to_cache(texture3)
texture3_w, texture3_h = 60, 60
texture3_cache = resize_cache_nearest(
    texture3_src_cache,
    texture3_src_w,
    texture3_src_h,
    texture3_w,
    texture3_h,
)

current_platform_texture_cache = texture_cache
current_platform_texture_w = texture_w
current_platform_texture_h = texture_h

# ================== TEXTURA FUNDO ESPACO (FASE 2) ==================
space_bg_texture = pygame.image.load("assets/images/fundoespaco.png")
space_bg_w, space_bg_h = space_bg_texture.get_width(), space_bg_texture.get_height()
space_bg_cache = surface_to_cache(space_bg_texture)

# ================== TEXTURA FUNDO DOCE (FASE 3) ==================
sweet_bg_texture = pygame.image.load("assets/images/fundodoce.png")
sweet_bg_w, sweet_bg_h = sweet_bg_texture.get_width(), sweet_bg_texture.get_height()
sweet_bg_cache = surface_to_cache(sweet_bg_texture)

# ================== TEXTURA ALIEN (FASE 2) ==================
alien_texture = pygame.image.load("assets/images/alien.png")
alien_src_w, alien_src_h = alien_texture.get_width(), alien_texture.get_height()
alien_src_cache = surface_to_cache(alien_texture)
alien_w, alien_h = 70, 70 
alien_cache = resize_cache_nearest(alien_src_cache, alien_src_w, alien_src_h, alien_w, alien_h)

# ================== TEXTURA MONSTRODOCE (FASE 3) ==================
monstrodoce_texture = pygame.image.load("assets/images/monstrodoce.png")
monstrodoce_src_w, monstrodoce_src_h = monstrodoce_texture.get_width(), monstrodoce_texture.get_height()
monstrodoce_src_cache = surface_to_cache(monstrodoce_texture)
monstrodoce_w, monstrodoce_h = 70, 70 
monstrodoce_cache = resize_cache_nearest(monstrodoce_src_cache, monstrodoce_src_w, monstrodoce_src_h, monstrodoce_w, monstrodoce_h)

# ================== TEXTURA PERSONAGEM ==================
garota_texture = pygame.image.load("assets/images/garota.png")
garota_src_w, garota_src_h = garota_texture.get_width(), garota_texture.get_height()
garota_src_cache = surface_to_cache(garota_texture)
garota_w, garota_h = 40, 60
garota_cache = resize_cache_nearest(garota_src_cache, garota_src_w, garota_src_h, garota_w, garota_h)

# ================== FONTE BITMAP ==================
BITMAP_FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10001", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
}

# ================== SET PIXEL (TRANSFORMAÇÃO DE COORDENADAS) ==================
# Transforma ponto do sistema de COORDENADAS DO MUNDO para
# COORDENADAS DE DISPOSITIVO (tela) e renderiza.
#
# Transformação aplicada:
#   sx = (x - offset_x) * zoom
#   sy = (y - offset_y) * zoom
#
# Onde:
#   (x, y) = coordenadas no mundo (espaço lógico do jogo)
#   (sx, sy) = coordenadas na tela (dispositivo)
#   offset_x, offset_y = translação (pan)
#   zoom = escala (zoom in/out)

def set_pixel(x, y, color):
    global draw_surface

    # Aplica transformação de coordenadas: mundo → dispositivo
    sx = int((x - offset_x) * zoom)
    sy = int((y - offset_y) * zoom)

    # Verifica se pixel está dentro da VIEWPORT (tela)
    if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
        draw_surface.set_at((sx, sy), color)

# ================== RECORTE DE COHEN-SUTHERLAND ==================
# Algoritmo de recorte de linha contra um retângulo (viewport).
# Recorta segmentos de linha que saem dos limites da janela.
# 
# VIEWPORT para recorte: [0, 0] a [WIDTH, HEIGHT]
# 
# Uso: cohen_sutherland(x1, y1, x2, y2) retorna (x1', y1', x2', y2')
#      ou None se a linha está completamente fora da viewport

INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0,1,2,4,8

def compute_code(x,y):
    """Computa o código de região para ponto (x, y) contra viewport."""
    code = INSIDE
    if x < 0: code |= LEFT
    elif x > WIDTH: code |= RIGHT
    if y < 0: code |= TOP
    elif y > HEIGHT: code |= BOTTOM
    return code

def cohen_sutherland(x1,y1,x2,y2):
    """Recorta linha (x1,y1)-(x2,y2) contra viewport [0,0]-[WIDTH,HEIGHT]."""
    code1 = compute_code(x1,y1)
    code2 = compute_code(x2,y2)

    while True:
        # Ambos dentro da viewport
        if code1 == 0 and code2 == 0:
            return x1,y1,x2,y2
        # Ambos fora do mesmo lado
        if code1 & code2:
            return None

        # Um ponto está fora
        code_out = code1 if code1 else code2

        # Calcula interseção com borda da viewport
        if code_out & TOP:
            x = x1 + (x2-x1)*(0-y1)/(y2-y1) if y2 != y1 else x1
            y = 0
        elif code_out & BOTTOM:
            x = x1 + (x2-x1)*(HEIGHT-y1)/(y2-y1) if y2 != y1 else x1
            y = HEIGHT
        elif code_out & RIGHT:
            y = y1 + (y2-y1)*(WIDTH-x1)/(x2-x1) if x2 != x1 else y1
            x = WIDTH
        elif code_out & LEFT:
            y = y1 + (y2-y1)*(0-x1)/(x2-x1) if x2 != x1 else y1
            x = 0

        # Atualiza ponto recortado
        if code_out == code1:
            x1,y1 = x,y
            code1 = compute_code(x1,y1)
        else:
            x2,y2 = x,y
            code2 = compute_code(x2,y2)

# ================== LINHA (COM RECORTE COHEN-SUTHERLAND) ==================
# Desenha linha com recorte automático contra a viewport.
# 
# Algoritmo:
#   1. Aplica Cohen-Sutherland para recortar linha contra viewport
#   2. Se linha está completamente fora, descarta
#   3. Caso contrário, desenha linha recortada com Bresenham

def draw_line(x0, y0, x1, y1, color):
    """Desenha linha de (x0,y0) até (x1,y1) com recorte Cohen-Sutherland."""
    # Aplica recorte de Cohen-Sutherland
    clipped = cohen_sutherland(x0,y0,x1,y1)
    if clipped is None:
        return  # Linha completamente fora da viewport

    x0,y0,x1,y1 = clipped
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    draw_px = set_pixel

    while True:
        draw_px(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def fill_polygon_scanline(vertices, color):
    if len(vertices) < 3:
        return

    min_y = max(0, math.ceil(min(v[1] for v in vertices)))
    max_y = min(HEIGHT - 1, math.floor(max(v[1] for v in vertices)))
    draw_px = set_pixel

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
            x_end = min(WIDTH - 1, math.floor(intersections[i + 1]))
            for x in range(x_start, x_end + 1):
                draw_px(x, y, color)


def fill_polygon_gradient_scanline(vertices, colors):
    if len(vertices) < 3 or len(vertices) != len(colors):
        return

    min_y = max(0, math.ceil(min(v[1] for v in vertices)))
    max_y = min(HEIGHT - 1, math.floor(max(v[1] for v in vertices)))
    draw_px = set_pixel

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
            xe = min(WIDTH - 1, math.floor(x2))
            span = x2 - x1

            for x in range(xs, xe + 1):
                t = 0 if span == 0 else (x - x1) / span
                r = int(r1 + t * (r2 - r1))
                g = int(g1 + t * (g2 - g1))
                b = int(b1 + t * (b2 - b1))
                draw_px(x, y, (r, g, b))


def fill_polygon_texture_scanline(vertices, tex_coords):
    if len(vertices) < 3 or len(vertices) != len(tex_coords):
        return

    min_y = max(0, math.ceil(min(v[1] for v in vertices)))
    max_y = min(HEIGHT - 1, math.floor(max(v[1] for v in vertices)))
    draw_px = set_pixel

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
            xe = min(WIDTH - 1, math.floor(x2))
            span = x2 - x1

            for x in range(xs, xe + 1):
                t = 0 if span == 0 else (x - x1) / span
                u = int(u1 + t * (u2 - u1)) % current_platform_texture_w
                v = int(v1 + t * (v2 - v1)) % current_platform_texture_h
                draw_px(x, y, current_platform_texture_cache[u][v])


def draw_text_bitmap(x, y, text, color, scale=2):
    cursor_x = x
    draw_px = set_pixel

    for ch in text.upper():
        glyph = BITMAP_FONT.get(ch, BITMAP_FONT[" "])
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == "1":
                    for sy in range(scale):
                        for sx in range(scale):
                            draw_px(cursor_x + gx * scale + sx, y + gy * scale + sy, color)
        cursor_x += (5 * scale) + scale


def bitmap_text_width(text, scale=2):
    if not text:
        return 0
    # Cada glifo tem 5 colunas + 1 coluna de espacamento.
    return (len(text) * (5 * scale + scale)) - scale


def draw_text_bitmap_centered(y, text, color, scale=2):
    text_w = bitmap_text_width(text, scale)
    x = (WIDTH - text_w) // 2
    draw_text_bitmap(x, y, text, color, scale)


def draw_rect_outline(x, y, w, h, color):
    draw_line(x, y, x + w, y, color)
    draw_line(x + w, y, x + w, y + h, color)
    draw_line(x + w, y + h, x, y + h, color)
    draw_line(x, y + h, x, y, color)

# ================== RETÂNGULO ==================
def draw_rect(x, y, w, h, color):
    vertices = [
        (x, y),
        (x + w, y),
        (x + w, y + h),
        (x, y + h),
    ]
    fill_polygon_scanline(vertices, color)

# ================== TEXTURA ==================
def draw_textured_rect(x,y,w,h):
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
    fill_polygon_texture_scanline(vertices, tex_coords)

# ================== ROTAÇÃO ==================
def rotate_point(px, py, cx, cy, angle):
    rad = math.radians(angle)
    x = px - cx
    y = py - cy

    xr = x * math.cos(rad) - y * math.sin(rad)
    yr = x * math.sin(rad) + y * math.cos(rad)

    return xr + cx, yr + cy

def draw_rotated_rect(p):
    cx = p["x"] + p["w"]/2
    cy = p["y"] + p["h"]/2

    corners = [
        (p["x"], p["y"]),
        (p["x"]+p["w"], p["y"]),
        (p["x"]+p["w"], p["y"]+p["h"]),
        (p["x"], p["y"]+p["h"])
    ]

    rotated = [rotate_point(x,y,cx,cy,p["angle"]) for x,y in corners]

    for i in range(4):
        x1,y1 = rotated[i]
        x2,y2 = rotated[(i+1)%4]
        draw_line(int(x1),int(y1),int(x2),int(y2),(255,200,100))


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


def check_rotated_platform_collision(p, player_rect):
    if p["type"] != "rotate":
        return None

    cx = p["x"] + p["w"] / 2
    cy = p["y"] + p["h"] / 2

    corners = [
        (p["x"], p["y"]),
        (p["x"] + p["w"], p["y"]),
        (p["x"] + p["w"], p["y"] + p["h"]),
        (p["x"], p["y"] + p["h"]),
    ]

    rotated = [rotate_point(x, y, cx, cy, p["angle"]) for x, y in corners]

    player_bottom_x = player_rect.centerx
    player_bottom_y = player_rect.bottom

    if point_in_polygon(player_bottom_x, player_bottom_y, rotated):
        support_y = get_polygon_support_y(player_bottom_x, rotated)
        if support_y is not None:
            return support_y

    return None

# ================== CÍRCULO ==================
def draw_circle(cx, cy, r, color):
    x = 0
    y = r
    d = 1 - r

    while x <= y:
        points = [
            (cx+x, cy+y), (cx-x, cy+y),
            (cx+x, cy-y), (cx-x, cy-y),
            (cx+y, cy+x), (cx-y, cy+x),
            (cx+y, cy-x), (cx-y, cy-x)
        ]
        for px, py in points:
            set_pixel(px, py, color)

        if d < 0:
            d += 2*x + 3
        else:
            d += 2*(x - y) + 5
            y -= 1
        x += 1

# ================== ELIPSE ==================
def draw_ellipse(cx, cy, rx, ry, color):
    for x in range(-rx, rx):
        y = int((1 - (x*x)/(rx*rx))**0.5 * ry)
        set_pixel(cx + x, cy + y, color)
        set_pixel(cx + x, cy - y, color)


def draw_filled_circle(cx, cy, r, color):
    for dy in range(-r, r + 1):
        dx = int((r * r - dy * dy) ** 0.5)
        draw_line(cx - dx, cy + dy, cx + dx, cy + dy, color)


def fill_textured_circle(cx, cy, r):
    white = (255, 255, 255, 255)
    for dy in range(-r, r + 1):
        dx = int((r * r - dy * dy) ** 0.5)
        for x in range(cx - dx, cx + dx + 1):
            set_pixel(x, cy + dy, white)


def draw_quarter_circle(cx, cy, r, color, quadrant="tr"):
    x = 0
    y = r
    d = 1 - r

    while x <= y:
        points = [
            (cx + x, cy - y), (cx + y, cy - x),
            (cx - x, cy - y), (cx - y, cy - x),
            (cx + x, cy + y), (cx + y, cy + x),
            (cx - x, cy + y), (cx - y, cy + x),
        ]

        for px, py in points:
            if quadrant == "tr" and px >= cx and py <= cy:
                set_pixel(px, py, color)
            elif quadrant == "tl" and px <= cx and py <= cy:
                set_pixel(px, py, color)
            elif quadrant == "br" and px >= cx and py >= cy:
                set_pixel(px, py, color)
            elif quadrant == "bl" and px <= cx and py >= cy:
                set_pixel(px, py, color)

        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1


def fill_textured_quarter_ring(cx, cy, inner_r, outer_r, color, quadrant="tl"):
    for dy in range(-outer_r, outer_r + 1):
        for dx in range(-outer_r, outer_r + 1):
            dist_sq = dx * dx + dy * dy
            if inner_r * inner_r <= dist_sq <= outer_r * outer_r:
                px = cx + dx
                py = cy + dy

                if quadrant == "tl" and px <= cx and py <= cy:
                    set_pixel(px, py, color)
                elif quadrant == "tr" and px >= cx and py <= cy:
                    set_pixel(px, py, color)
                elif quadrant == "bl" and px <= cx and py >= cy:
                    set_pixel(px, py, color)
                elif quadrant == "br" and px >= cx and py >= cy:
                    set_pixel(px, py, color)


def draw_cloud(cx, cy, scale=1.0):
    s = scale
    clouds = [
        (cx - int(28 * s), cy + int(4 * s), int(18 * s)),
        (cx - int(10 * s), cy - int(10 * s), int(22 * s)),
        (cx + int(12 * s), cy - int(14 * s), int(20 * s)),
        (cx + int(34 * s), cy - int(8 * s), int(19 * s)),
        (cx + int(54 * s), cy + int(4 * s), int(16 * s)),
        (cx - int(6 * s), cy + int(10 * s), int(17 * s)),
        (cx + int(18 * s), cy + int(12 * s), int(18 * s)),
    ]

    for px, py, radius in clouds:
        fill_textured_circle(px, py, radius)

    # Pequeno acabamento na base para deixar a nuvem mais próxima da referência.
    fill_textured_circle(cx + int(30 * s), cy + int(12 * s), int(10 * s))
    fill_textured_circle(cx - int(16 * s), cy + int(12 * s), int(11 * s))


def draw_rainbow(x, y):
    rainbow_colors = [
        (255, 0, 0, 255),      # vermelho
        (255, 127, 0, 255),    # laranja
        (255, 255, 0, 255),    # amarelo
        (0, 200, 0, 255),      # verde
        (80, 190, 255, 255),   # azul claro
        (0, 70, 200, 255),     # azul escuro
        (128, 0, 200, 255),    # roxo
    ]
    base_inner = 58
    band_thickness = 8
    for i, color in enumerate(rainbow_colors):
        inner = base_inner + i * band_thickness
        outer = inner + band_thickness
        fill_textured_quarter_ring(x, y, inner, outer, color, quadrant="tl")


def build_level1_background_surface():
    global draw_surface
    saved_surface = draw_surface

    level_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_surface = level_surface

    fill_polygon_scanline(
        [(0, 0), (WIDTH - 1, 0), (WIDTH - 1, HEIGHT - 1), (0, HEIGHT - 1)],
        (168, 224, 255),
    )

    draw_filled_circle(95, 95, 22, (255, 230, 70))
    draw_circle(95, 95, 22, (255, 210, 40))

    draw_cloud(150, 160, scale=1.1)
    draw_cloud(85, 255, scale=0.95)
    draw_cloud(640, 105, scale=1.2)
    draw_cloud(500, 230, scale=1.0)

    # Ancora o arco-iris na plataforma de chegada (goal) da fase 1.
    goal_platform = next((p for p in platforms if p["type"] == "goal"), None)
    if goal_platform is not None:
        draw_rainbow(WIDTH - 1, goal_platform["y"])
    else:
        draw_rainbow(WIDTH - 1, 175)

    draw_surface = saved_surface
    return level_surface


def fill_textured_background(tex_cache, tex_w, tex_h):
    """Preenche o fundo inteiro com textura em modo tiling."""
    draw_px = set_pixel
    for y in range(HEIGHT):
        for x in range(WIDTH):
            tx = x % tex_w
            ty = y % tex_h
            draw_px(x, y, tex_cache[tx][ty])


def build_level2_background_surface():
    global draw_surface
    saved_surface = draw_surface

    level_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_surface = level_surface

    fill_textured_background(space_bg_cache, space_bg_w, space_bg_h)

    draw_surface = saved_surface
    return level_surface


def build_level3_background_surface():
    global draw_surface
    saved_surface = draw_surface

    level_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_surface = level_surface

    fill_textured_background(sweet_bg_cache, sweet_bg_w, sweet_bg_h)

    draw_surface = saved_surface
    return level_surface


def rect_circle_collision(rect, cx, cy, r):
    nearest_x = max(rect.left, min(cx, rect.right))
    nearest_y = max(rect.top, min(cy, rect.bottom))
    dx = cx - nearest_x
    dy = cy - nearest_y
    return dx * dx + dy * dy <= r * r


def update_enemies():
    for enemy in enemies:
        enemy["x"] += enemy["dir"] * enemy["speed"]
        if enemy["x"] <= enemy["min_x"] or enemy["x"] >= enemy["max_x"]:
            enemy["dir"] *= -1
            enemy["x"] = max(enemy["min_x"], min(enemy["x"], enemy["max_x"]))


def draw_enemies():
    for enemy in enemies:
        if level == 2:
            # Fase 2: desenha alien usando textura
            cx = int(enemy["x"])
            cy = int(enemy["y"])
            half_w = alien_w // 2
            half_h = alien_h // 2
            draw_px = set_pixel
            for dy in range(alien_h):
                for dx in range(alien_w):
                    color = alien_cache[dx][dy]
                    if color[3] > 128:  # Só desenha se não é transparente
                        px = cx - half_w + dx
                        py = cy - half_h + dy
                        draw_px(px, py, color)
        elif level == 3:
            # Fase 3: desenha monstrodoce usando textura
            cx = int(enemy["x"])
            cy = int(enemy["y"])
            half_w = monstrodoce_w // 2
            half_h = monstrodoce_h // 2
            draw_px = set_pixel
            for dy in range(monstrodoce_h):
                for dx in range(monstrodoce_w):
                    color = monstrodoce_cache[dx][dy]
                    if color[3] > 128:  # Só desenha se não é transparente
                        px = cx - half_w + dx
                        py = cy - half_h + dy
                        draw_px(px, py, color)
        else:
            # Fase 1: desenha bola verde
            draw_filled_circle(int(enemy["x"]), int(enemy["y"]), enemy["r"], (90, 190, 90))
            draw_circle(int(enemy["x"]), int(enemy["y"]), enemy["r"], (40, 110, 40))
            set_pixel(int(enemy["x"] - 5), int(enemy["y"] - 2), (255, 255, 255))
            set_pixel(int(enemy["x"] + 5), int(enemy["y"] - 2), (255, 255, 255))

# ================== FLOOD FILL ==================
def flood_fill(x, y, target_color, new_color):
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

        if px < 0 or px >= WIDTH or py < 0 or py >= HEIGHT:
            continue

        if draw_surface.get_at((px, py))[:3] != target_color:
            continue

        set_pixel(px, py, new_color)

        stack.append((px+1, py))
        stack.append((px-1, py))
        stack.append((px, py+1))
        stack.append((px, py-1))

# ================== PLAYER ==================
player = pygame.Rect(100, 400, 30, 30)
vel_y = 0
gravity = 0.5
jump = -10
on_ground = False

# ================== ESTADO ==================
game_state = "menu"

# ================== NÍVEL ==================
level = 1

# ================== PLATAFORMAS ==================
platforms = []
enemies = []
static_platform_cache = defaultdict(dict)

def create_level():
    global platforms, enemies, current_platform_texture_cache, current_platform_texture_w, current_platform_texture_h

    if level == 2:
        current_platform_texture_cache = texture2_cache
        current_platform_texture_w = texture2_w
        current_platform_texture_h = texture2_h
    elif level == 3:
        current_platform_texture_cache = texture3_cache
        current_platform_texture_w = texture3_w
        current_platform_texture_h = texture3_h
    else:
        current_platform_texture_cache = texture_cache
        current_platform_texture_w = texture_w
        current_platform_texture_h = texture_h

    if level == 1:
        platforms = [
            {"x":60, "y":540, "w":150, "h":20, "type":"static"},
            {"x":240, "y":500, "w":120, "h":20, "type":"move", "dir":1, "speed":1.6, "min_x":200, "max_x":300},
            {"x":430, "y":450, "w":110, "h":20, "type":"static"},
            {"x":610, "y":390, "w":110, "h":20, "type":"scale", "scale":1, "growing":True},
            {"x":460, "y":320, "w":80, "h":20, "type":"static"},
            {"x":280, "y":270, "w":100, "h":20, "type":"static"},
            {"x":505, "y":190, "w":120, "h":20, "type":"static"},
            {"x":690, "y":130, "w":90, "h":20, "type":"goal"}
        ]
        enemies = []

    elif level == 2:
        platforms = [
            {"x":40, "y":540, "w":150, "h":20, "type":"static"},
            {"x":190, "y":490, "w":110, "h":20, "type":"move", "dir":1, "speed":2.0, "min_x":150, "max_x":280},
            {"x":360, "y":415, "w":110, "h":20, "type":"static"},
            {"x":550, "y":360, "w":105, "h":20, "type":"scale", "scale":1, "growing":True},
            {"x":400, "y":280, "w":80, "h":20, "type":"static"},
            {"x":200, "y":230, "w":120, "h":20, "type":"static"},
            {"x":450, "y":165, "w":120, "h":20, "type":"static"},
            {"x":700, "y":100, "w":80, "h":20, "type":"goal"}
        ]
        enemies = [
            {"x":575, "y":340, "r":15, "dir":1, "speed":1.5, "min_x":525, "max_x":635}
        ]

    elif level == 3:
        platforms = [
            {"x":30, "y":540, "w":130, "h":20, "type":"static"},
            {"x":200, "y":510, "w":110, "h":20, "type":"static"},
            {"x":330, "y":435, "w":110, "h":20, "type":"move", "dir":1, "speed":2.0, "min_x":280, "max_x":460},
            {"x":180, "y":380, "w":110, "h":20, "type":"static"},
            {"x":350, "y":300, "w":80, "h":20, "type":"static"},
            {"x":660, "y":240, "w":90, "h":20, "type":"move", "dir":-1, "speed":2.3, "min_x":480, "max_x":650},
            {"x":400, "y":152, "w":80, "h":20, "type":"static"},
            {"x":580, "y":110, "w":30, "h":10, "type":"static"},
            {"x":700, "y":80, "w":80, "h":20, "type":"goal"}
        ]
        enemies = [
            {"x":225, "y":360, "r":15, "dir":1, "speed":1.5, "min_x":200, "max_x":300},
            # {"x":610, "y":278, "r":16, "dir":-1, "speed":2.0, "min_x":550, "max_x":690}
        ]

    # Reseta cache da fase para garantir consistencia apos troca.
    static_platform_cache[level].clear()

create_level()

# ================== GRADIENTE ==================
def draw_gradient():
    for y in range(HEIGHT):
        color = (50 + int(50*y/HEIGHT), 50, 100 + int(100*y/HEIGHT))
        for x in range(WIDTH):
            set_pixel(x, y, color)


def render_static_platform_surface(p):
    key = (int(p["w"]), int(p["h"]))
    if key in static_platform_cache[level]:
        return static_platform_cache[level][key]

    global draw_surface
    saved_surface = draw_surface

    # Sem alpha aqui para manter o topo visual alinhado ao topo de colisao,
    # igual ao comportamento das plataformas desenhadas direto na tela.
    platform_surface = pygame.Surface(key)
    draw_surface = platform_surface

    # Desenha usando as mesmas funcoes de rasterizacao por pixel.
    draw_textured_rect(0, 0, key[0], key[1])

    draw_surface = saved_surface
    static_platform_cache[level][key] = platform_surface
    return platform_surface


def build_gradient_surface():
    global draw_surface
    saved_surface = draw_surface

    gradient_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_surface = gradient_surface
    draw_gradient()

    draw_surface = saved_surface
    return gradient_surface


level1_background_surface = build_level1_background_surface()
level2_background_surface = build_level2_background_surface()
level3_background_surface = build_level3_background_surface()


def build_menu_surface():
    global draw_surface
    saved_surface = draw_surface

    menu_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_surface = menu_surface

    fill_polygon_scanline(
        [(0, 0), (WIDTH - 1, 0), (WIDTH - 1, HEIGHT - 1), (0, HEIGHT - 1)],
        (20, 20, 30),
    )
    draw_circle(600, 150, 50, (255,255,255))
    draw_ellipse(150, 100, 60, 30, (255,182,193))
    draw_line(0, 500, 800, 500, (255,255,255))
    flood_fill(600,150,(20,20,30),(200,200,255))
    draw_text_bitmap_centered(250, "SONHOS EM CONSTRUCAO", (255, 255, 255), scale=3)
    draw_text_bitmap_centered(320, "PRESSIONE ENTER", (255, 255, 255), scale=2)
    draw_text_bitmap_centered(355, "APERTE ESC PARA SAIR", (220, 220, 255), scale=2)

    draw_surface = saved_surface
    return menu_surface


gradient_surface = build_gradient_surface()
menu_surface = build_menu_surface()


def build_win_surface():
    global draw_surface
    saved_surface = draw_surface

    win_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_surface = win_surface

    fill_polygon_scanline(
        [(0, 0), (WIDTH - 1, 0), (WIDTH - 1, HEIGHT - 1), (0, HEIGHT - 1)],
        (20, 20, 30),
    )
    draw_rect_outline(120, 180, 560, 220, (120, 150, 220))
    draw_text_bitmap_centered(235, "SONHO COMPLETO!", (255, 255, 255), scale=3)
    draw_text_bitmap_centered(300, "APERTE R PARA REINICIAR", (200, 220, 255), scale=2)
    draw_text_bitmap_centered(335, "APERTE ESC PARA SAIR", (200, 220, 255), scale=2)

    draw_surface = saved_surface
    return win_surface


win_surface = build_win_surface()


def build_dead_surface():
    global draw_surface
    saved_surface = draw_surface

    dead_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_surface = dead_surface

    fill_polygon_scanline(
        [(0, 0), (WIDTH - 1, 0), (WIDTH - 1, HEIGHT - 1), (0, HEIGHT - 1)],
        (25, 15, 20),
    )
    draw_rect_outline(120, 180, 560, 220, (220, 120, 120))
    draw_text_bitmap_centered(235, "VOCE CAIU!", (255, 210, 210), scale=3)
    draw_text_bitmap_centered(300, "APERTE R PARA REINICIAR", (240, 240, 255), scale=2)
    draw_text_bitmap_centered(335, "APERTE ESC PARA SAIR", (240, 240, 255), scale=2)

    draw_surface = saved_surface
    return dead_surface


dead_surface = build_dead_surface()

# ================== MENU ==================
def draw_menu():
    screen.blit(menu_surface, (0, 0))

# ================== UPDATE ==================
def update_platforms():
    for p in platforms:
        if p["type"] == "move":
            p["_prev_x"] = p["x"]
            p["x"] += p.get("speed", 2) * p["dir"]
            if p["x"] > p.get("max_x", p["x"]) or p["x"] < p.get("min_x", p["x"]):
                p["dir"] *= -1
                p["x"] = max(p.get("min_x", p["x"]), min(p["x"], p.get("max_x", p["x"])))

        elif p["type"] == "scale":
            if p["growing"]:
                p["scale"] += 0.01
                if p["scale"] >= 1.5:
                    p["growing"] = False
            else:
                p["scale"] -= 0.01
                if p["scale"] <= 0.5:
                    p["growing"] = True

            p["w"] = 100 * p["scale"]

        elif p["type"] == "rotate":
            p["angle"] += 1

# ================== DRAW ==================
def draw_platforms():
    for p in platforms:
        if p["type"] == "static":
            surface = render_static_platform_surface(p)
            screen.blit(surface, (int(p["x"]), int(p["y"])))
        elif p["type"] == "goal":
            vertices = [
                (p["x"], p["y"]),
                (p["x"] + p["w"], p["y"]),
                (p["x"] + p["w"], p["y"] + p["h"]),
                (p["x"], p["y"] + p["h"]),
            ]
            colors = [
                (255, 220, 80),
                (255, 150, 60),
                (255, 90, 40),
                (255, 180, 70),
            ]
            fill_polygon_gradient_scanline(vertices, colors)
            draw_rect_outline(p["x"], p["y"], p["w"], p["h"], (255, 220, 80))
        elif p["type"] == "rotate":
            draw_textured_rect(p["x"], p["y"], p["w"], p["h"])
            draw_rect_outline(p["x"], p["y"], p["w"], p["h"], (255, 220, 80))
        else:
            draw_textured_rect(p["x"], p["y"], p["w"], p["h"])


def draw_enemies_on_screen():
    draw_enemies()

def draw_player():
    draw_px = set_pixel
    # Centralizar horizontalmente e alinhar os pés com o topo da caixa de colisão
    offset_x = (garota_w - player.width) // 2
    offset_y = garota_h - player.height
    draw_x = player.x - offset_x
    draw_y = player.y - offset_y
    
    for dx in range(garota_w):
        for dy in range(garota_h):
            color = garota_cache[dx][dy]
            if color[3] > 128:
                draw_px(draw_x + dx, draw_y + dy, color)

# ================== PLAYER ==================
def move_player():
    global vel_y, on_ground
    keys = pygame.key.get_pressed()
    supporting_platform = None

    # remember previous position for robust collision resolution
    prev_x, prev_y = player.x, player.y

    # Sprite da personagem e maior que a hitbox (30x30).
    # Usamos esse offset para impedir que a cabeca visual atravesse plataformas.
    sprite_x_offset = (garota_w - player.width) // 2
    sprite_head_offset = garota_h - player.height

    # horizontal input
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5

    # Resolve horizontal collisions before applying gravity.
    for p in platforms:
        if p["type"] == "rotate":
            continue

        rect = pygame.Rect(p["x"], p["y"], p["w"], p["h"])
        if not player.colliderect(rect):
            continue

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            player.left = rect.right
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            player.right = rect.left
        else:
            if prev_x + player.width <= rect.left:
                player.right = rect.left
            elif prev_x >= rect.right:
                player.left = rect.right
            elif player.centerx < rect.centerx:
                player.right = rect.left
            else:
                player.left = rect.right

        if p["type"] == "goal":
            return "win"

    # vertical physics
    vel_y += gravity
    player.y += vel_y

    if player.y > HEIGHT + 100:
        return "dead"

    on_ground = False

    # check collisions against platforms (AABB), handle rotated separately
    for p in platforms:
        if p["type"] == "rotate":
            support_y = check_rotated_platform_collision(p, player)
            if support_y is not None and vel_y >= 0:
                player.bottom = int(support_y)
                vel_y = 0
                on_ground = True
                supporting_platform = p
        else:
            rect = pygame.Rect(p["x"], p["y"], p["w"], p["h"])

            # Colisao da cabeca visual com a base da plataforma (quando sobe).
            if vel_y < 0:
                prev_visual_top = prev_y - sprite_head_offset
                curr_visual_top = player.y - sprite_head_offset
                visual_left = player.x - sprite_x_offset
                visual_right = visual_left + garota_w

                horizontal_overlap = visual_right > rect.left and visual_left < rect.right
                crossed_platform_bottom = prev_visual_top >= rect.bottom and curr_visual_top <= rect.bottom

                if horizontal_overlap and crossed_platform_bottom:
                    player.top = rect.bottom + sprite_head_offset
                    vel_y = 0
                    continue

            if player.colliderect(rect):
                # vertical resolution
                came_from_above = prev_y + player.height <= rect.top
                came_from_below = prev_y >= rect.bottom

                if came_from_above and vel_y >= 0:
                    # falling onto platform
                    player.bottom = rect.top
                    vel_y = 0
                    on_ground = True
                    supporting_platform = p
                elif came_from_below and vel_y < 0:
                    # hitting head on underside
                    player.top = rect.bottom + sprite_head_offset
                    vel_y = 0
                else:
                    # Safety fallback in case the player spawns inside a platform.
                    if player.centerx < rect.centerx:
                        player.right = rect.left
                    else:
                        player.left = rect.right

                if p["type"] == "goal":
                    return "win"

    # if standing on a moving platform, move with it
    if supporting_platform and supporting_platform.get("type") == "move":
        move_dx = supporting_platform.get("x", 0) - supporting_platform.get("_prev_x", supporting_platform.get("x", 0))
        player.x += move_dx

        # Recheck side collisions after being carried by a moving platform.
        # This prevents phase 2/3 platforms from being crossed horizontally.
        if move_dx != 0:
            for p in platforms:
                if p is supporting_platform or p["type"] == "rotate":
                    continue

                rect = pygame.Rect(p["x"], p["y"], p["w"], p["h"])
                if not player.colliderect(rect):
                    continue

                if move_dx > 0:
                    player.right = rect.left
                else:
                    player.left = rect.right

                if p["type"] == "goal":
                    return "win"

    # enemy collisions
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for enemy in enemies:
        if rect_circle_collision(player_rect, int(enemy["x"]), int(enemy["y"]), enemy["r"]):
            return "dead"

    # jump
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump

    return None

# ================== WIN ==================
def draw_win():
    screen.blit(win_surface, (0, 0))


def draw_dead():
    screen.blit(dead_surface, (0, 0))

# ================== LOOP ==================
while True:
    clock.tick(60)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]: zoom += 0.01
    if keys[pygame.K_e]: zoom -= 0.01

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "menu" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_state = "game"

        elif game_state == "menu" and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        elif game_state == "win" and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            level = 1
            player.x, player.y = 100, 400
            vel_y = 0
            create_level()
            game_state = "game"

        elif game_state == "dead" and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            level = 1
            player.x, player.y = 100, 400
            vel_y = 0
            create_level()
            game_state = "game"

        elif game_state in ("win", "dead") and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if game_state == "menu":
        draw_menu()

    elif game_state == "game":
        if level == 1:
            screen.blit(level1_background_surface, (0, 0))
        elif level == 2:
            screen.blit(level2_background_surface, (0, 0))
        else:
            screen.blit(level3_background_surface, (0, 0))
        update_platforms()
        update_enemies()

        result = move_player()
        if result == "dead":
            game_state = "dead"
        elif result == "win":
            level += 1
            if level > 3:
                game_state = "win"
            else:
                player.x, player.y = 100, 400
                vel_y = 0
                create_level()

        draw_platforms()
        draw_enemies_on_screen()
        draw_player()

    elif game_state == "win":
        draw_win()

    elif game_state == "dead":
        draw_dead()

    pygame.display.flip()