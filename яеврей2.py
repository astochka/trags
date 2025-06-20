import pygame, random

pygame.init()
w, h = 500, 500
sc = pygame.display.set_mode((w, h))
pygame.display.set_caption("Aim Trainer")

font = pygame.font.SysFont("gabriola", 28, bold=True)
small_font = pygame.font.SysFont("gabriola", 24, bold=True)

levels = {
    'Легко': {'size_range': (40, 60), 'move_interval': 2000},
    'Средне': {'size_range': (20, 50), 'move_interval': 1200},
    'Тяжело': {'size_range': (5, 40), 'move_interval': 700},
}
current_level = 'Средне'
circle_color = (255, 100, 100)

hits = misses = 0
start_ticks = pygame.time.get_ticks()
last_move = pygame.time.get_ticks()
x = y = r = 0

def is_hit(x, y, mx, my, r):
    dx, dy = x - mx, y - my
    return dx * dx + dy * dy <= r * r

def randomize():
    global x, y, r
    sz_min, sz_max = levels[current_level]['size_range']
    r = random.randint(sz_min, sz_max)
    x = random.randint(r, w - r)
    y = random.randint(r + 50, h - r - 50)

def draw_circle():
    pygame.draw.circle(sc, circle_color, (x, y), r)
    pygame.draw.circle(sc, (255, 255, 255), (x, y), r, 3)

def get_background():
    if hits > 15: return (160, 100, 255)
    if hits > 10: return (100, 255, 160)
    if hits > 5: return (100, 160, 255)
    return (30, 30, 30)

def get_quote():
    if hits > 15: return "🔝 Ти машина!"
    if hits > 10: return "🔥 Оце точність!"
    if hits > 5:  return "👏 Добре йде!"
    if hits > 0:  return "🙂 Початок є!"
    return "🔘 Натисни на коло!"

def draw_text_with_frame(surface, text, font, pos, base_color, frame_color):
    text_surf = font.render(text, True, base_color)
    rect = text_surf.get_rect(topleft=pos)
    padding = 10
    frame_rect = pygame.Rect(rect.left - padding//2, rect.top - padding//2,
                             rect.width + padding, rect.height + padding)
    # Неоновая подложка
    s = pygame.Surface((frame_rect.width, frame_rect.height), pygame.SRCALPHA)
    s.fill((*frame_color, 100))
    surface.blit(s, (frame_rect.left, frame_rect.top))
    # Контур
    pygame.draw.rect(surface, frame_color, frame_rect, 2, border_radius=8)
    surface.blit(text_surf, pos)

randomize()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if is_hit(x, y, mx, my, r):
                hits += 1
                randomize()
                last_move = pygame.time.get_ticks()
            else:
                misses += 1
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_1: current_level = 'Легко'
            if e.key == pygame.K_2: current_level = 'Средне'
            if e.key == pygame.K_3: current_level = 'Тяжело'
            hits = misses = 0
            start_ticks = pygame.time.get_ticks()
            randomize()

    if pygame.time.get_ticks() - last_move > levels[current_level]['move_interval']:
        randomize()
        last_move = pygame.time.get_ticks()

    sc.fill(get_background())
    draw_circle()

    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000

    # Строка сверху
    draw_text_with_frame(sc, f"🎯 {hits}   💨 {misses}   ⏱️ {elapsed_time}s   ⚙️ {current_level}",
                         font, (10, 10), (0, 255, 255), (0, 100, 255))

    # Цитата снизу
    quote_text = get_quote()
    quote_surf = small_font.render(quote_text, True, (255, 255, 255))
    quote_rect = quote_surf.get_rect(center=(w // 2, h - 30))
    # Полупрозрачный фон + рамка
    s = pygame.Surface((quote_rect.width + 20, quote_rect.height + 10), pygame.SRCALPHA)
    s.fill((255, 0, 255, 90))
    sc.blit(s, (quote_rect.left - 10, quote_rect.top - 5))
    pygame.draw.rect(sc, (255, 0, 255), (quote_rect.left - 10, quote_rect.top - 5,
                                         quote_rect.width + 20, quote_rect.height + 10), 2, border_radius=8)
    sc.blit(quote_surf, quote_rect)

    pygame.display.flip()