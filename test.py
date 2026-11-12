import pygame
import random
import os

pygame.init()

WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20
TOP_BAR = 120
GAME_WIDTH = WIDTH
GAME_HEIGHT = HEIGHT - TOP_BAR
FPS = 10
WINNING_SCORE = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boa Hancock - Navy Hunt")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (15, 15, 20)
GREEN = (40, 180, 90)
DARK_GREEN = (20, 100, 50)
RED = (220, 35, 45)
GOLD = (230, 190, 60)
GRAY = (100, 100, 110)
PURPLE = (130, 60, 170)

font = pygame.font.SysFont("Arial", 24, bold=True)
small_font = pygame.font.SysFont("Arial", 18)
big_font = pygame.font.SysFont("Arial", 42, bold=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")

def load_image(filename, size):
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.isfile(path):
        return None
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, size)
    except pygame.error:
        return None

boa_image = load_image("boa.png", (65, 65))
dragon_image = load_image("celestial_dragon.png", (65, 65))
boa_win_image = load_image("boa_win.png", (200, 200))

boa_score = 0
dragon_score = 0

def create_snake():
    return [
        [200, 200],
        [180, 200],
        [160, 200]
    ]

snake = create_snake()
direction = "RIGHT"
next_direction = "RIGHT"

def create_food():
    cols = WIDTH // CELL_SIZE
    rows = (HEIGHT - TOP_BAR) // CELL_SIZE
    while True:
        x = random.randrange(cols) * CELL_SIZE
        y = TOP_BAR + random.randrange(rows) * CELL_SIZE
        if [x, y] not in snake:
            return [x, y]

food = create_food()
game_over = False
winner = None

def draw_scoreboard():
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, TOP_BAR))

    if boa_image:
        screen.blit(boa_image, (20, 15))
    else:
        pygame.draw.rect(screen, PURPLE, (20, 15, 65, 65))

    boa_name = font.render("BOA HANCOCK", True, WHITE)
    boa_points = big_font.render(str(boa_score), True, GOLD)

    screen.blit(boa_name, (100, 15))
    screen.blit(boa_points, (100, 48))

    if dragon_image:
        screen.blit(dragon_image, (WIDTH - 85, 15))
    else:
        pygame.draw.rect(screen, GRAY, (WIDTH - 85, 15, 65, 65))

    dragon_name = small_font.render("CELESTIAL DRAGON", True, WHITE)
    dragon_points = big_font.render(str(dragon_score), True, GOLD)

    screen.blit(dragon_name, (WIDTH - 210, 15))
    screen.blit(dragon_points, (WIDTH - 210, 48))

    pygame.draw.line(screen, GRAY, (0, TOP_BAR - 2), (WIDTH, TOP_BAR - 2), 2)

def draw_snake():
    for index, segment in enumerate(snake):
        x, y = segment
        if index == 0:
            pygame.draw.circle(screen, DARK_GREEN, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2)
            pygame.draw.circle(screen, WHITE, (x + 7, y + 6), 3)
            pygame.draw.circle(screen, WHITE, (x + 14, y + 6), 3)
        else:
            pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE), border_radius=6)

def draw_food():
    x, y = food
    pygame.draw.rect(screen, RED, (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=5)
    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 3)

def reset_round():
    global snake, direction, next_direction, food, game_over, winner
    snake = create_snake()
    direction = "RIGHT"
    next_direction = "RIGHT"
    food = create_food()
    game_over = False
    winner = None

def end_round():
    global game_over, dragon_score, winner
    if not game_over:
        game_over = True
        dragon_score += 1
        if dragon_score >= WINNING_SCORE:
            winner = "CELESTIAL DRAGON"

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_over:
                if event.key == pygame.K_r and winner is None:
                    reset_round()
                if event.key == pygame.K_RETURN and winner is not None:
                    boa_score = 0
                    dragon_score = 0
                    reset_round()
            else:
                if event.key in (pygame.K_UP, pygame.K_w):
                    if direction != "DOWN":
                        next_direction = "UP"
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if direction != "UP":
                        next_direction = "DOWN"
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if direction != "RIGHT":
                        next_direction = "LEFT"
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if direction != "LEFT":
                        next_direction = "RIGHT"

    if not game_over:
        direction = next_direction
        head_x, head_y = snake[0]

        if direction == "UP":
            head_y -= CELL_SIZE
        elif direction == "DOWN":
            head_y += CELL_SIZE
        elif direction == "LEFT":
            head_x -= CELL_SIZE
        elif direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = [head_x, head_y]

        if (head_x < 0 or head_x >= WIDTH or head_y < TOP_BAR or head_y >= HEIGHT):
            end_round()
        else:
            eating = new_head == food
            body_to_check = snake if eating else snake[:-1]

            if new_head in body_to_check:
                end_round()
            else:
                snake.insert(0, new_head)
                if eating:
                    boa_score += 1
                    food = create_food()
                    if boa_score >= WINNING_SCORE:
                        game_over = True
                        winner = "BOA HANCOCK"
                else:
                    snake.pop()

    screen.fill((35, 100, 65))
    draw_scoreboard()

    pygame.draw.rect(screen, (65, 130, 85), (0, TOP_BAR, WIDTH, GAME_HEIGHT))

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (75, 140, 95), (x, TOP_BAR), (x, HEIGHT))
    for y in range(TOP_BAR, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (75, 140, 95), (0, y), (WIDTH, y))

    draw_food()
    draw_snake()

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(190)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        if winner:
            if winner == "BOA HANCOCK" and boa_win_image:
                img_x = (WIDTH // 2) - 100
                img_y = (HEIGHT // 2) - 150
                screen.blit(boa_win_image, (img_x, img_y))
                
                title = big_font.render(winner + " WINS!", True, GOLD)
                screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80)))
                
                message = font.render("Press ENTER to restart the match", True, WHITE)
                screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130)))
            else:
                title = big_font.render(winner + " WINS!", True, GOLD)
                screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
                message = font.render("Press ENTER to restart the match", True, WHITE)
                screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
        else:
            title = big_font.render("SALOME LOST!", True, RED)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
            message = font.render("The Celestial Dragon gets 1 point!", True, WHITE)
            screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))

        if winner is None:
            restart = small_font.render("Press R to play another round", True, WHITE)
            screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 55)))

    pygame.display.flip()

pygame.quit()