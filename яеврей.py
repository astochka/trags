import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600,400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird with Cats")
clock = pygame.time.Clock()

# Загрузка фона и персонажа
background = pygame.transform.scale(pygame.image.load("яв.jpg"), (WIDTH, HEIGHT))
character = pygame.transform.scale(pygame.image.load("zzz.png"), (60, 60))

x, y = 100, 200
velocity_y = 0
gravity = 0.35
jump_power = -6
pipe_speed = 5

font = pygame.font.SysFont("arialblack", 36)
tip_font = pygame.font.SysFont("verdana", 22)

obstacles = []
obstacle_timer = 0
obstacle_width = 60
gap_height = 160
min_distance = 100

score = 0

# Загрузка труб с прозрачным фоном
pipe_top_raw = pygame.image.load("zz.png").convert_alpha()
pipe_bottom_raw = pygame.image.load("zs.png").convert_alpha()

def generate_pipe_colors():
    return (
        random.randint(50, 255),
        random.randint(50, 255),
        random.randint(50, 255)
    )

running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            velocity_y = jump_power

    velocity_y += gravity
    y += velocity_y
    y = max(0, min(y, HEIGHT - 60))

    obstacle_timer += 1
    if obstacle_timer > min_distance:
        top_height = random.randint(50, HEIGHT - gap_height - 50)
        bottom_height = HEIGHT - top_height - gap_height

        top_obstacle = pygame.Rect(WIDTH, 0, obstacle_width, top_height)
        bottom_obstacle = pygame.Rect(WIDTH, HEIGHT - bottom_height, obstacle_width, bottom_height)

        color = generate_pipe_colors()
        passed = False

        obstacles.append([top_obstacle, bottom_obstacle, top_height, bottom_height, color, passed])
        obstacle_timer = 0

    cat = pygame.Rect(x, y, 60, 60)

    for obs in obstacles[:]:
        top, bottom, h_top, h_bottom, color, passed = obs

        top.x -= pipe_speed
        bottom.x -= pipe_speed

        if cat.colliderect(top) or cat.colliderect(bottom):
            print("Game Over!")
            pygame.quit()
            exit()

        if not passed and top.x + obstacle_width < x:
            obs[5] = True
            score += 1

        if top.right < 0:
            obstacles.remove(obs)

        # Фон трубы (цвет)
        top_color_rect = pygame.Surface((obstacle_width, h_top))
        top_color_rect.fill(color)
        screen.blit(top_color_rect, (top.x, top.y))

        bottom_color_rect = pygame.Surface((obstacle_width, h_bottom))
        bottom_color_rect.fill(color)
        screen.blit(bottom_color_rect, (bottom.x, bottom.y))

        # Картинка кота поверх трубы
        top_pipe_img = pygame.transform.scale(pipe_top_raw, (obstacle_width, h_top))
        bottom_pipe_img = pygame.transform.scale(pipe_bottom_raw, (obstacle_width, h_bottom))

        screen.blit(top_pipe_img, (top.x, top.y))
        screen.blit(bottom_pipe_img, (bottom.x, bottom.y))

    screen.blit(character, (x, y))

    # Счёт
    score_surf = font.render(f"{score}", True, (255, 255, 255))
    screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()