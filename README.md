# Sonhos em Construção

## Sobre o Projeto

**Sonhos em Construção** é um jogo 2D desenvolvido em Python utilizando a biblioteca :contentReference[oaicite:0]{index=0}.  
O jogo acompanha a personagem **Luna** em uma jornada pelos seus sonhos, passando por diferentes mundos:

- Céu Azul
- Espaço
- Mundo dos Doces

Cada fase representa desafios, medos e conquistas da personagem, utilizando conceitos de **Computação Gráfica**, como rasterização, transformações geométricas, clipping, texturização e algoritmos clássicos de desenho.

---

# Funcionalidades do Jogo

- Sistema de menu inicial
- Três fases temáticas
- Plataformas estáticas e móveis
- Plataformas com escala dinâmica
- Sistema de colisão
- Inimigos animados
- Música de fundo
- Sistema de vitória e derrota
- Personagem com textura personalizada
- Cenários totalmente desenhados manualmente por rasterização
- Suporte a zoom e viewport

---

# Conceitos de Computação Gráfica Utilizados

O projeto implementa diversos conceitos fundamentais da disciplina:

## Rasterização

Renderização manual de pixels utilizando:

- `set_pixel()`
- `draw_line()`
- `draw_circle()`
- `draw_rect()`

---

## Algoritmo de Bresenham

Utilizado para desenho de linhas.

Função:
```python
draw_line()
```

---

## Algoritmo de Cohen-Sutherland

Utilizado para recorte de linhas contra a viewport.

Função:
```python
cohen_sutherland()
```

---

## Transformações Geométricas

Implementação de:

- Translação
- Escala
- Rotação
- Zoom

Funções:
```python
rotate_point()
draw_rotated_rect()
```

---

## Viewport e Transformação de Coordenadas

Conversão de coordenadas do mundo para coordenadas da tela.

Fórmula utilizada:

```text
sx = (x - offset_x) * zoom
sy = (y - offset_y) * zoom
```

---

## Preenchimento de Polígonos (Scanline)

Implementado manualmente para:

- Polígonos sólidos
- Gradientes
- Texturas

Funções:
```python
fill_polygon_scanline()
fill_polygon_gradient_scanline()
fill_polygon_texture_scanline()
```

---

## Texturização

As plataformas, personagens e cenários utilizam texturas carregadas via imagem.

---

## Colisão

Sistema de colisão entre:

- Jogador e plataformas
- Jogador e inimigos
- Plataformas rotacionadas

---

## Flood Fill

Implementação do algoritmo Flood Fill.

Função:
```python
flood_fill()
```

---

# Controles

| Tecla | Ação |
|---|---|
| ← → | Movimentação |
| Espaço | Pular |
| Enter | Iniciar jogo |
| R | Reiniciar |
| ESC | Sair |
| Q | Zoom In |
| E | Zoom Out |

---

# Estrutura do Projeto

```text
projeto/
│
├── main.py
├── README.md
│
├── game/
│   ├── main_game.py
│   ├── engine/
│       ├── image_cache.py
│       ├── geometry.py
│       └── bitmap_font.py
│   └── funcionalidades/
│       ├── pixel_viewport.py
│       ├── clipping.py
│       ├── rasterizacao.py
│       ├── preenchimento.py
│       ├── transformacoes.py
│       ├── texturizacao.py
│       ├── animacao.py
│       ├── input_handler.py
│       └── menus.py
│
├── assets/
│   ├── music/
│   │   └── musica.mp3
│   │
│   └── images/
│       ├── plataforma.png
│       ├── plataforma2.png
│       ├── plataforma3.png
│       ├── fundoespaco.png
│       ├── fundodoce.png
│       ├── alien.png
│       ├── monstrodoce.png
│       ├── garota.png
│       └── casaluna.png
```

---

# Fases do Jogo

## Fase 1 — Céu Azul

Primeira etapa da jornada de Luna.

Características:
- Céu claro
- Nuvens desenhadas proceduralmente
- Arco-íris
- Plataformas móveis

---

## Fase 2 — Espaço

Representa os medos e incertezas.

Características:
- Fundo espacial texturizado
- Inimigos alienígenas
- Plataformas dinâmicas

---

## Fase 3 — Mundo dos Doces

Última fase da jornada.

Características:
- Cenário doce
- Monstros temáticos
- Plataformas mais difíceis

---

# Personagem

A protagonista do jogo é **Luna**, representando a trajetória de sonhos, desafios e conquistas.

A personagem utiliza:
- Sprite com transparência
- Sistema de colisão independente da textura
- Movimentação com gravidade

---

# Requisitos

## Linguagem
- Python 3.10+

## Bibliotecas
- Pygame

---

# Instalação

## 1. Instalar Python

Baixe em:

[Python Oficial](https://www.python.org/downloads/?utm_source=chatgpt.com)

---

## 2. Instalar Pygame

No terminal:

```bash
pip install pygame
```

---

# ▶Execução

Execute o arquivo principal:

```bash
python main.py
```

---

# Recursos Utilizados

## Áudio
- Música de fundo em loop

## Imagens
- Sprites personalizados
- Texturas para plataformas
- Fundos texturizados

---

# Principais Funções Implementadas

| Função | Descrição |
|---|---|
| `set_pixel()` | Desenha pixels manualmente |
| `draw_line()` | Desenha linhas |
| `draw_circle()` | Desenha círculos |
| `fill_polygon_scanline()` | Preenchimento de polígonos |
| `fill_polygon_texture_scanline()` | Preenchimento com textura |
| `rotate_point()` | Rotação de pontos |
| `cohen_sutherland()` | Clipping de linhas |
| `move_player()` | Física e movimentação |
| `update_platforms()` | Atualização das plataformas |
| `draw_player()` | Renderização do jogador |

---

# Técnicas Extras Implementadas

- Cache de texturas
- Resize manual de imagens
- Sistema de renderização otimizado
- Backgrounds pré-renderizados
- Bitmap font personalizada
- Plataformas com transformação dinâmica

---

# Objetivo Educacional

Este projeto foi desenvolvido com o objetivo de aplicar na prática os conceitos estudados na disciplina de **Computação Gráfica**, implementando manualmente algoritmos fundamentais sem utilizar primitivas prontas da biblioteca gráfica.

---

# Desenvolvedores

- Integrante 1: Olga Pedrosa de Sousa 
- Integrante 2: Marília Milfont Rangel Lima

