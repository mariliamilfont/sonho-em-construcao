import pygame
import sys
import math
import os
from collections import defaultdict

# Permite executar tanto por `python main.py` quanto direto por `python game/main_game.py`.
if __package__ is None or __package__ == "":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.engine.image_cache import (
    surface_to_cache as cache_surface_to_cache,
    resize_cache_nearest as cache_resize_cache_nearest,
)
from game.engine.geometry import (
    check_rotated_platform_collision as geom_check_rotated_platform_collision,
    rect_circle_collision as geom_rect_circle_collision,
)
from game.engine.bitmap_font import (
    draw_text_bitmap as font_draw_text_bitmap,
    draw_text_bitmap_centered as font_draw_text_bitmap_centered,
)
from game.funcionalidades.pixel_viewport import set_pixel as feature_set_pixel
from game.funcionalidades.clipping import cohen_sutherland as feature_cohen_sutherland
from game.funcionalidades.rasterizacao import (
    draw_line as feature_draw_line,
    draw_circle as feature_draw_circle,
    draw_ellipse as feature_draw_ellipse,
    draw_filled_circle as feature_draw_filled_circle,
)
from game.funcionalidades.preenchimento import (
    fill_polygon_scanline as feature_fill_polygon_scanline,
    fill_polygon_gradient_scanline as feature_fill_polygon_gradient_scanline,
    fill_polygon_texture_scanline as feature_fill_polygon_texture_scanline,
    flood_fill as feature_flood_fill,
)
from game.funcionalidades.transformacoes import rotate_point as feature_rotate_point
from game.funcionalidades.texturizacao import (
    draw_textured_rect as feature_draw_textured_rect,
    fill_textured_background as feature_fill_textured_background,
)
from game.funcionalidades.animacao import (
    update_enemies as feature_update_enemies,
    update_platforms as feature_update_platforms,
)
from game.funcionalidades.input_handler import (
    apply_zoom_keys as feature_apply_zoom_keys,
    handle_state_event as feature_handle_state_event,
)
from game.funcionalidades.menus import (
    draw_menu as feature_draw_menu,
    draw_win as feature_draw_win,
    draw_dead as feature_draw_dead,
)

pygame.init()
pygame.mixer.init()

# ================== MUSICA ==================
pygame.mixer.music.load("assets/music/musica.mp3")
pygame.mixer.music.set_volume(0.2)  
pygame.mixer.music.play(-1)  # loop infinito

# ================== VIEWPORT ==================
# Coordenadas de Dispositivo (Tela): 800x600 pixels
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sonhos em Construção")

clock = pygame.time.Clock()

draw_surface = screen

zoom = 1.0
offset_x = 0
offset_y = 0


# ================== TEXTURA ==================
texture = pygame.image.load("assets/images/plataforma.png")
texture_src_w, texture_src_h = texture.get_width(), texture.get_height()
texture_src_cache = cache_surface_to_cache(texture)
texture_w, texture_h = 50, 50
texture_cache = cache_resize_cache_nearest(
    texture_src_cache,
    texture_src_w,
    texture_src_h,
    texture_w,
    texture_h,
)

texture2 = pygame.image.load("assets/images/plataforma2.png")
texture2_src_w, texture2_src_h = texture2.get_width(), texture2.get_height()
texture2_src_cache = cache_surface_to_cache(texture2)
texture2_w, texture2_h = 50, 50
texture2_cache = cache_resize_cache_nearest(
    texture2_src_cache,
    texture2_src_w,
    texture2_src_h,
    texture2_w,
    texture2_h,
)

texture3 = pygame.image.load("assets/images/plataforma3.png")
texture3_src_w, texture3_src_h = texture3.get_width(), texture3.get_height()
texture3_src_cache = cache_surface_to_cache(texture3)
texture3_w, texture3_h = 60, 60
texture3_cache = cache_resize_cache_nearest(
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
space_bg_cache = cache_surface_to_cache(space_bg_texture)

# ================== TEXTURA FUNDO DOCE (FASE 3) ==================
sweet_bg_texture = pygame.image.load("assets/images/fundodoce.png")
sweet_bg_w, sweet_bg_h = sweet_bg_texture.get_width(), sweet_bg_texture.get_height()
sweet_bg_cache = cache_surface_to_cache(sweet_bg_texture)

# ================== TEXTURA ALIEN (FASE 2) ==================
alien_texture = pygame.image.load("assets/images/alien.png")
alien_src_w, alien_src_h = alien_texture.get_width(), alien_texture.get_height()
alien_src_cache = cache_surface_to_cache(alien_texture)
alien_w, alien_h = 70, 70 
alien_cache = cache_resize_cache_nearest(alien_src_cache, alien_src_w, alien_src_h, alien_w, alien_h)

# ================== TEXTURA MONSTRODOCE (FASE 3) ==================
monstrodoce_texture = pygame.image.load("assets/images/monstrodoce.png")
monstrodoce_src_w, monstrodoce_src_h = monstrodoce_texture.get_width(), monstrodoce_texture.get_height()
monstrodoce_src_cache = cache_surface_to_cache(monstrodoce_texture)
monstrodoce_w, monstrodoce_h = 70, 70 
monstrodoce_cache = cache_resize_cache_nearest(monstrodoce_src_cache, monstrodoce_src_w, monstrodoce_src_h, monstrodoce_w, monstrodoce_h)

# ================== TEXTURA PERSONAGEM ==================
garota_texture = pygame.image.load("assets/images/garota.png")
garota_src_w, garota_src_h = garota_texture.get_width(), garota_texture.get_height()
garota_src_cache = cache_surface_to_cache(garota_texture)
garota_w, garota_h = 40, 60
garota_cache = cache_resize_cache_nearest(garota_src_cache, garota_src_w, garota_src_h, garota_w, garota_h)

# ================== TEXTURA CASA ==================
casa_texture = pygame.image.load("assets/images/casaluna.png")
casa_src_w, casa_src_h = casa_texture.get_width(), casa_texture.get_height()
casa_src_cache = cache_surface_to_cache(casa_texture)
casa_w, casa_h = 320, 400
casa_cache = cache_resize_cache_nearest(casa_src_cache, casa_src_w, casa_src_h, casa_w, casa_h)

# ================== SET PIXEL (TRANSFORMAÇÃO DE COORDENADAS) ==================

def rotate_point(x, y, cx, cy, angle):
    rad = math.radians(angle)
    
    # Translada para origem
    tx = x - cx
    ty = y - cy
    
    # Rotação
    rx = tx * math.cos(rad) - ty * math.sin(rad)
    ry = tx * math.sin(rad) + ty * math.cos(rad)
    
    # Volta para posição original
    return int(rx + cx), int(ry + cy)

def set_pixel(x, y, color):
    global draw_surface
    feature_set_pixel(draw_surface, WIDTH, HEIGHT, offset_x, offset_y, zoom, x, y, color)

# ================== RECORTE DE COHEN-SUTHERLAND ==================
def cohen_sutherland(x1,y1,x2,y2):
    return feature_cohen_sutherland(x1, y1, x2, y2, WIDTH, HEIGHT)

# ================== LINHA (COM RECORTE COHEN-SUTHERLAND) ==================
def draw_line(x0, y0, x1, y1, color):
    feature_draw_line(x0, y0, x1, y1, color, set_pixel, cohen_sutherland)


def fill_polygon_scanline(vertices, color):
    feature_fill_polygon_scanline(vertices, color, WIDTH, HEIGHT, set_pixel)


def fill_polygon_gradient_scanline(vertices, colors):
    feature_fill_polygon_gradient_scanline(vertices, colors, WIDTH, HEIGHT, set_pixel)


def fill_polygon_texture_scanline(vertices, tex_coords):
    feature_fill_polygon_texture_scanline(
        vertices,
        tex_coords,
        WIDTH,
        HEIGHT,
        set_pixel,
        current_platform_texture_cache,
        current_platform_texture_w,
        current_platform_texture_h,
    )


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
    feature_draw_textured_rect(x, y, w, h, fill_polygon_texture_scanline)

def draw_rotated_rect(p):
    cx = p["x"] + p["w"]/2
    cy = p["y"] + p["h"]/2

    corners = [
        (p["x"], p["y"]),
        (p["x"]+p["w"], p["y"]),
        (p["x"]+p["w"], p["y"]+p["h"]),
        (p["x"], p["y"]+p["h"])
    ]

    rotated = [feature_rotate_point(x, y, cx, cy, p["angle"], math) for x, y in corners]

    for i in range(4):
        x1,y1 = rotated[i]
        x2,y2 = rotated[(i+1)%4]
        draw_line(int(x1),int(y1),int(x2),int(y2),(255,200,100))

# ================== CÍRCULO ==================
def draw_circle(cx, cy, r, color):
    feature_draw_circle(cx, cy, r, color, set_pixel)

# ================== ELIPSE ==================
def draw_ellipse(cx, cy, rx, ry, color):
    feature_draw_ellipse(cx, cy, rx, ry, color, set_pixel)


def draw_filled_circle(cx, cy, r, color):
    feature_draw_filled_circle(cx, cy, r, color, draw_line)


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
    feature_fill_textured_background(WIDTH, HEIGHT, tex_cache, tex_w, tex_h, set_pixel)


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


def update_enemies():
    feature_update_enemies(enemies)


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
    feature_flood_fill(x, y, target_color, new_color, WIDTH, HEIGHT, draw_surface, set_pixel)

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


def draw_stars(count=100):
    """Desenha estrelas espalhadas no céu noturno."""
    import random
    random.seed(42)  # Para sempre gerar as mesmas estrelas
    for _ in range(count):
        x = random.randint(0, WIDTH)
        y = random.randint(0, int(HEIGHT * 0.6))
        size = random.randint(1, 3)
        brightness = random.randint(180, 255)
        set_pixel(x, y, (brightness, brightness, brightness))
        # Adiciona pequeno brilho ao redor da estrela
        if size > 1:
            for dx in [-1, 1]:
                if 0 <= x + dx < WIDTH:
                    set_pixel(x + dx, y, (brightness // 2, brightness // 2, brightness // 2))
            for dy in [-1, 1]:
                if 0 <= y + dy < int(HEIGHT * 0.6):
                    set_pixel(x, y + dy, (brightness // 2, brightness // 2, brightness // 2))


def draw_moon(cx, cy, radius):
    """Desenha uma lua cheia com cor uniforme."""
    # Desenha círculo principal da lua em cor amarelada uniforme
    draw_filled_circle(cx, cy, radius, (255, 250, 200))


def draw_night_sky():
    """Desenha um céu noturno com gradiente."""
    # Céu com gradiente de azul escuro para mais escuro
    for y in range(HEIGHT):
        # Gradiente: mais azul no topo, mais escuro embaixo
        ratio = y / HEIGHT
        r = int(10 + 30 * ratio)
        g = int(15 + 35 * ratio)
        b = int(40 + 50 * ratio)
        for x in range(WIDTH):
            set_pixel(x, y, (r, g, b))


def draw_house(x, y, scale=1.0):
    """Desenha uma casa pixelada no estilo retrocom escala ajustavel."""
    s = scale
    # Parede principal (amarelo)
    fill_polygon_scanline(
        [(x, y + int(40*s)), (x + int(60*s), y + int(40*s)), (x + int(60*s), y + int(80*s)), (x, y + int(80*s))],
        (220, 180, 80)
    )
    
    # Telhado (triangulo vermelho)
    fill_polygon_scanline(
        [(x - int(5*s), y + int(40*s)), (x + int(65*s), y + int(40*s)), (x + int(30*s), y + int(10*s))],
        (200, 60, 60)
    )
    
    # Porta (retangulo marrom)
    fill_polygon_scanline(
        [(x + int(20*s), y + int(60*s)), (x + int(40*s), y + int(60*s)), (x + int(40*s), y + int(80*s)), (x + int(20*s), y + int(80*s))],
        (100, 60, 30)
    )
    
    # Maaneta (pequeno circulo)
    draw_filled_circle(x + int(38*s), y + int(70*s), int(2*s), (200, 180, 100))
    
    # Janela 1 (esquerda)
    fill_polygon_scanline(
        [(x + int(8*s), y + int(48*s)), (x + int(18*s), y + int(48*s)), (x + int(18*s), y + int(58*s)), (x + int(8*s), y + int(58*s))],
        (150, 200, 255)
    )
    draw_rect_outline(x + int(8*s), y + int(48*s), int(10*s), int(10*s), (80, 120, 180))
    
    # Janela 2 (direita)
    fill_polygon_scanline(
        [(x + int(42*s), y + int(48*s)), (x + int(52*s), y + int(48*s)), (x + int(52*s), y + int(58*s)), (x + int(42*s), y + int(58*s))],
        (150, 200, 255)
    )
    draw_rect_outline(x + int(42*s), y + int(48*s), int(10*s), int(10*s), (80, 120, 180))
    
    # Chimene (retangulo marrom escuro)
    fill_polygon_scanline(
        [(x + int(50*s), y + int(15*s)), (x + int(58*s), y + int(15*s)), (x + int(58*s), y + int(40*s)), (x + int(50*s), y + int(40*s))],
        (80, 40, 20)
    )


def draw_ufo_with_ellipses(cx, cy, scale=1.0):
    s = scale

    # Base do OVNI: preenchimento manual por múltiplas elipses.
    base_rx = int(120 * s)
    base_ry = int(42 * s)
    for ry in range(base_ry, 0, -1):
        draw_ellipse(cx, cy, base_rx, ry, (82, 97, 108))
    draw_ellipse(cx, cy, base_rx, base_ry, (120, 136, 148))

    # Cúpula superior.
    dome_cx = cx
    dome_cy = cy - int(34 * s)
    dome_rx = int(52 * s)
    dome_ry = int(28 * s)
    for ry in range(dome_ry, 0, -1):
        draw_ellipse(dome_cx, dome_cy, dome_rx, ry, (84, 214, 218))
    draw_ellipse(dome_cx, dome_cy, dome_rx, dome_ry, (60, 190, 200))

    # Brilho da cúpula.
    draw_ellipse(dome_cx + int(16 * s), dome_cy - int(9 * s), int(14 * s), int(6 * s), (225, 225, 210))

    # Luzes da base.
    lights = 6
    for i in range(lights):
        lx = cx - int(88 * s) + int(i * (176 * s) / (lights - 1))
        ly = cy - int(1 * s)
        draw_filled_circle(lx, ly, int(6 * s), (110, 240, 120))
        draw_circle(lx, ly, int(6 * s), (85, 210, 110))

def draw_rotating_image(cx, cy, image_cache, angle):
    h = len(image_cache)
    w = len(image_cache[0])

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    # centro da imagem original
    ox = w // 2
    oy = h // 2

    for x in range(w):
        for y in range(h):
            color = image_cache[x][y]

            # ignora transparência
            if color[3] < 128:
                continue

            # coordenadas relativas ao centro
            tx = x - ox
            ty = y - oy

            # 🔄 rotação geométrica (ESSENCIAL)
            rx = tx * cos_a - ty * sin_a
            ry = tx * sin_a + ty * cos_a

            # posição final na tela
            screen_x = int(cx + rx)
            screen_y = int(cy + ry)

            set_pixel(screen_x, screen_y, color)

def build_menu_surface():
    global draw_surface
    saved_surface = draw_surface

    menu_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_surface = menu_surface

    # Desenha céu noturno com gradiente
    draw_night_sky()
    
    # Adiciona estrelas
    draw_stars(120)
    
    # Desenha lua cheia no canto superior direito
    draw_moon(700, 100, 60)
    
    # Adiciona algumas nuvens no ceu
    draw_cloud(130, 170, scale=1.1)
    draw_cloud(500, 140, scale=0.95)
    draw_cloud(660, 260, scale=1.2)

    # OVNI no canto inferior direito da abertura (requisito de uso de elipse).
    draw_ufo_with_ellipses(680, 530, scale=0.95)
    
    # Desenha a casa no lado esquerdo, maior e mais perto do chao
    #draw_house(42, 290, scale=2.3)

    # Desenha a imagem da casa (casaluna.png)
    draw_px = set_pixel

    for dx in range(casa_w):
        for dy in range(casa_h):
            color = casa_cache[dx][dy]

            # desenha apenas pixels não transparentes
            if color[3] > 128:
                draw_px(-25 + dx, 180 + dy, color)
    

    # Texto do menu - Titulo (maior e mais distante das nuvens)
    font_draw_text_bitmap_centered(40, "SONHOS EM CONSTRUÇÃO", (255, 255, 200), WIDTH, set_pixel, scale=4)
    
    # Texto da historia
    history_lines = [
        "Venha acompanhar Luna na jornada dos seus sonhos:",
        "pelo ceu azul, onde tudo parecia possivel,",
        "atravessando o espaco, enfrentando medos e incertezas,",
        "ate encontrar um mundo de doces,",
        "onde, pouco a pouco, constroi seus mais belos sonhos."
    ]
    
    y_pos = 200
    for line in history_lines:
        font_draw_text_bitmap(250, y_pos, line, (200, 220, 255), set_pixel, scale=1)
        y_pos += 35
    
    # Botao e instrucoes (mais perto do chao)
    draw_rect_outline(230, 480, 340, 50, (150, 180, 225))
    font_draw_text_bitmap_centered(505, "PRESSIONE ENTER PARA COMECAR", (200, 220, 255), WIDTH, set_pixel, scale=1)
    
    font_draw_text_bitmap_centered(545, "APERTE ESC PARA SAIR", (180, 190, 220), WIDTH, set_pixel, scale=1)

    draw_surface = saved_surface
    return menu_surface


gradient_surface = build_gradient_surface()
menu_surface = build_menu_surface()


def build_win_surface():
    global draw_surface
    saved_surface = draw_surface

    win_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_surface = win_surface

    draw_night_sky()
    draw_stars(120)

    draw_rect_outline(120, 180, 560, 220, (120, 150, 220))
    font_draw_text_bitmap_centered(235, "SONHO COMPLETO!", (255, 255, 255), WIDTH, set_pixel, scale=3)
    font_draw_text_bitmap_centered(300, "APERTE R PARA REINICIAR", (200, 220, 255), WIDTH, set_pixel, scale=2)
    font_draw_text_bitmap_centered(335, "APERTE ESC PARA SAIR", (200, 220, 255), WIDTH, set_pixel, scale=2)

    draw_surface = saved_surface
    return win_surface


win_surface = build_win_surface()


def build_dead_surface():
    global draw_surface
    saved_surface = draw_surface

    dead_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_surface = dead_surface

    draw_night_sky()
    draw_stars(120)

    draw_rect_outline(120, 180, 560, 220, (220, 120, 120))
    font_draw_text_bitmap_centered(235, "VOCE CAIU!", (255, 210, 210), WIDTH, set_pixel, scale=3)
    font_draw_text_bitmap_centered(300, "APERTE R PARA REINICIAR", (240, 240, 255), WIDTH, set_pixel, scale=2)
    font_draw_text_bitmap_centered(335, "APERTE ESC PARA SAIR", (240, 240, 255), WIDTH, set_pixel, scale=2)

    draw_surface = saved_surface
    return dead_surface


dead_surface = build_dead_surface()

# ================== MENU ==================
def draw_menu():
    feature_draw_menu(screen, menu_surface)

# ================== UPDATE ==================
def update_platforms():
    feature_update_platforms(platforms)

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

    prev_x, prev_y = player.x, player.y

    # Sprite da personagem e maior que a hitbox (30x30).
    # Usamos esse offset para impedir que a cabeca visual atravesse plataformas.
    sprite_x_offset = (garota_w - player.width) // 2
    sprite_head_offset = garota_h - player.height

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

    vel_y += gravity
    player.y += vel_y

    if player.y > HEIGHT + 100:
        return "dead"

    on_ground = False

    for p in platforms:
        if p["type"] == "rotate":
            support_y = geom_check_rotated_platform_collision(p, player, math)
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
               
                came_from_above = prev_y + player.height <= rect.top
                came_from_below = prev_y >= rect.bottom

                if came_from_above and vel_y >= 0:
               
                    player.bottom = rect.top
                    vel_y = 0
                    on_ground = True
                    supporting_platform = p
                elif came_from_below and vel_y < 0:
                    
                    player.top = rect.bottom + sprite_head_offset
                    vel_y = 0
                else:
            
                    if player.centerx < rect.centerx:
                        player.right = rect.left
                    else:
                        player.left = rect.right

                if p["type"] == "goal":
                    return "win"

    if supporting_platform and supporting_platform.get("type") == "move":
        move_dx = supporting_platform.get("x", 0) - supporting_platform.get("_prev_x", supporting_platform.get("x", 0))
        player.x += move_dx

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

    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for enemy in enemies:
        if geom_rect_circle_collision(player_rect, int(enemy["x"]), int(enemy["y"]), enemy["r"]):
            return "dead"

    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump

    return None

# ================== WIN ==================
def draw_win():
    feature_draw_win(screen, win_surface)


def draw_dead():
    feature_draw_dead(screen, dead_surface)

alien_angle = 0

# ================== LOOP ==================
while True:
    clock.tick(60)

    alien_angle += 1  # controla velocidade

    keys = pygame.key.get_pressed()
    zoom = feature_apply_zoom_keys(keys, zoom, pygame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        _, level, vel_y, should_quit, next_state = feature_handle_state_event(
            event, game_state, level, player, vel_y, create_level, pygame
        )
        if should_quit:
            pygame.quit()
            sys.exit()
        if next_state is not None:
            game_state = next_state
            if next_state == "game":
                create_level()

    if game_state == "menu":
        draw_menu()
        draw_rotating_image(700, 450, alien_cache, alien_angle)

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