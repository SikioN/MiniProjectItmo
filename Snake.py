import time
from random import randrange

import pygame

RES = 1000
SIZE = 50

x, y = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)

apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
gold_apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)

gold_random = randrange(1, 100)

length = 1
snake = [(x, y)]

dx, dy = 0, 0
fps = 144
dirs = {"W": True, "S": True, "A": True, "D": True}
speed_count, snake_speed = 0, 25
length_count = 0
snake_color = [
    "#BDFFA4",
    "#A0E989",
    "#86CC6F",
    "#6AB155",
    "#4F963C",
    "#337B24",
    "#136207",
]
color = 0

score = 0
timing = time.time()
flag = False

pygame.init()
font_score = pygame.font.SysFont("ArcadeClassic", SIZE, bold=True)
background = pygame.display.set_mode([RES, RES])
background_img = pygame.image.load("background.png").convert()
clock = pygame.time.Clock()


def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


while True:
    background.blit(background_img, (0, 0))
    [
        pygame.draw.rect(
            background, pygame.Color(snake_color[color]), (i, j, SIZE - 1, SIZE - 1)
        )
        for i, j in snake
    ]
    pygame.draw.rect(background, pygame.Color("red"), (apple[0], apple[1], SIZE, SIZE))
    render_score = font_score.render(
        f"YOUR SCORE: {score}", True, pygame.Color("white")
    )
    background.blit(render_score, (5, 5))

    # if flag:
    #     pygame.draw.rect(background, pygame.Color('gold'), (gold_apple[0], gold_apple[1], SIZE, SIZE))

    speed_count += 1

    # if gold_random == 1 and not flag:
    #     time_gold_apple = time.time()
    #     point_gold_apple = 3
    #     timing = time.time()
    #     flag = True
    #     gold_random = randrange(2, 1000)
    # else:
    #     gold_random = randrange(2, 10000)

    if not speed_count % snake_speed:
        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        snake = snake[-length:]

    # if time.time() - timing > 2.5:
    #     pygame.draw.rect(background, pygame.Color('black'), (gold_apple[0], gold_apple[1], SIZE, SIZE))
    #     gold_apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    #     timing = 0
    #     flag = False

    if snake[-1] == apple:
        apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
        if length > 4:
            if length_count == 3:
                length += 1
                length_count = 0
            else:
                length_count += 1
        else:
            length += 1

        score += 1

        if score % 5 == 0 and color != len(snake_color) - 1:
            color += 1

        snake_speed -= 1
        snake_speed = max(snake_speed, 10)

    # if snake[-1] == gold_apple and flag:
    #     gold_apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    #     length += 2
    #     snake_speed -= 1
    #     flag = True
    #     snake_speed = max(snake_speed, 5)

    if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE:
        if y < -SIZE:
            y = RES
        elif y > RES:
            y = -SIZE
        if x < -SIZE:
            x = RES
        elif x > RES:
            x = -SIZE

    pygame.display.flip()
    clock.tick(fps)
    close_game()

    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        if dirs["W"]:
            dx, dy = 0, -1
            dirs = {
                "W": True,
                "S": False,
                "A": True,
                "D": True,
            }
    elif key[pygame.K_s]:
        if dirs["S"]:
            dx, dy = 0, 1
            dirs = {
                "W": False,
                "S": True,
                "A": True,
                "D": True,
            }
    elif key[pygame.K_a]:
        if dirs["A"]:
            dx, dy = -1, 0
            dirs = {
                "W": True,
                "S": True,
                "A": True,
                "D": False,
            }
    elif key[pygame.K_d]:
        if dirs["D"]:
            dx, dy = 1, 0
            dirs = {
                "W": True,
                "S": True,
                "A": False,
                "D": True,
            }
