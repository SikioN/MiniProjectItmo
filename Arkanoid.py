import pygame
from random import randrange

RES = 1000
fps = 144

paddle_w = 250
paddle_h = 25
paddle_speed = 10
paddle = pygame.Rect(RES // 2 - paddle_w // 2, RES - paddle_h - 10, paddle_w, paddle_h)

ball_radius = 25
ball_speed = 4
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(
    randrange(ball_rect, RES - ball_rect), RES // 2, ball_rect, ball_rect
)
dx, dy = 1, -1

block_list = [
    pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)
]
color_list = [
    (randrange(30, 256), randrange(30, 256), randrange(30, 256))
    for i in range(10)
    for j in range(4)
]

pygame.init()
font_end = pygame.font.SysFont("ArcadeClassic", 50, bold=True)
clock = pygame.time.Clock()
background = pygame.display.set_mode([RES, RES])
background_img = pygame.image.load("background2.png").convert()


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


while True:
    background.blit(background_img, (0, 0))
    [
        pygame.draw.rect(background, color_list[color], block)
        for color, block in enumerate(block_list)
    ]
    pygame.draw.rect(background, pygame.Color("#00009c"), paddle)
    pygame.draw.circle(background, pygame.Color("lightgrey"), ball.center, ball_radius)

    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    if ball.centerx < ball_radius or ball.centerx > RES - ball_radius:
        dx = -dx
    if ball.centery < ball_radius:
        dy = -dy
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(background, hit_color, hit_rect)
        fps += 2

    if ball.bottom > RES:
        while True:
            render_end = font_end.render("GAME OVER", True, pygame.Color("lightgrey"))
            background.blit(render_end, (RES // 2 - 125, RES // 2 - 100))
            pygame.display.flip()
            close_game()

    pygame.display.flip()
    clock.tick(fps)

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] or key[pygame.K_a] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] or key[pygame.K_w] and paddle.right < RES:
        paddle.right += paddle_speed
