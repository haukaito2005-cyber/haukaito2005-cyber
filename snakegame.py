import pygame
import random
import sys
import math

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

# ======================
# màu sắc
# ======================
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
SKY_BLUE = (0, 191, 255)

# tạo cửa sổ
glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# font
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

# ======================
# game states
# ======================
MAIN_MENU = 0
DIFFICULTY_MENU = 1
PLAYING = 2
SETTINGS = 3
GAME_OVER = 4
game_state = MAIN_MENU

# ======================
# cài đặt độ khó
# ======================
difficulty = 1 # 1=Easy, 2=Medium, 3=Hard
snake_speed = 10
score_per_food = 1

# ======================
# hệ thống skin
# ======================
skin_level = 1

def set_difficulty(level):
    global difficulty
    global snake_speed
    global score_per_food
    difficulty = level
    if level == 1:
        snake_speed = 10
        score_per_food = 1
    elif level == 2:
        snake_speed = 15
        score_per_food = 2
    elif level == 3:
        snake_speed = 20
        score_per_food = 3
       
def update_skin():
    global skin_level
    if score >= 40:
        skin_level = 5
    elif score >= 30:
        skin_level = 4
    elif score >= 20:
        skin_level = 3
    elif score >= 10:
        skin_level = 2
    else:
        skin_level = 1        

def create_food(snake):
    while True:
        food = (
            random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        )
        if food not in snake:
            return food

# ======================
# vẽ lưới
# ======================
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

# ======================
# reset game
# ======================
def reset_game():
    global skin_level
    skin_level = 1
    level_message = ""
    message_timer = 0
    snake = [(300, 300)]
    direction = (CELL_SIZE, 0)
    food = create_food(snake)
    score = 0
    return snake, direction, food, score

# menu
def draw_difficulty_menu():
    screen.fill(BLACK)
    title = big_font.render(
        "Select Difficulty",
        True,
        WHITE
    )
    easy = font.render(
        "1 - Easy",
        True,
        GREEN
    )
    medium = font.render(
        "2 - Medium",
        True,
        WHITE
    )
    hard = font.render(
        "3 - Hard",
        True,
        RED
    )
    screen.blit(title, (120, 150))
    screen.blit(easy, (220, 260))
    screen.blit(medium, (200, 320))
    screen.blit(hard, (220, 380))

def draw_main_menu():
    screen.fill(BLACK)
    title = big_font.render(
        "Snake Game",
        True,
        GREEN
    )
    start = font.render(
        "Press ENTER To Start",
        True,
        WHITE
    )
    quit_text = font.render(
        "Press Q To Quit",
        True,
        WHITE
    )
    screen.blit(title, (150, 180))
    screen.blit(start, (140, 300))
    screen.blit(quit_text, (170, 350))

def draw_game():
        # vẽ mồi
        brightness = 150 + int(50 * math.sin(pygame.time.get_ticks() * 0.01))
        size_offset = int(3 * math.sin(pygame.time.get_ticks() * 0.01))
        food_size = CELL_SIZE + size_offset
        pygame.draw.rect(
            screen,
            (brightness, 0, 0),
            (
                food[0] - size_offset // 2,
                food[1] - size_offset // 2,
                food_size,
                food_size
            ),
            border_radius=5
        )

        # vẽ hiệu ứng sáng cho mồi
        screen.blit(glow_surface, (0, 0))

        # vẽ rắn săn mồi
        if skin_level == 1:
            head_color = SKY_BLUE
            body_color = DARK_GREEN
        elif skin_level == 2:
            head_color = RED
            body_color = (255, 165, 0)
        elif skin_level == 3:
            head_color = (255, 255, 0)
            body_color = (255, 215, 0)
        elif skin_level == 4:
            head_color = (255, 0, 255)
            body_color = (128, 0, 255)
        else:
            rainbow_colors = [
                (255, 0, 0),
                (255, 127, 0),
                (255, 255, 0),
                (0, 255, 0),
                (0, 0, 255),
                (75, 0, 130),
                (148, 0, 211)
            ]

        for i, segment in enumerate(snake):
            x, y = segment
            if skin_level == 5:
                offset = pygame.time.get_ticks() // 100
                color = rainbow_colors[
                    (i + offset) % len(rainbow_colors)
                ]
            else:
                color = head_color if i == 0 else body_color
            pygame.draw.rect(
                screen,
                color,
                (x, y, CELL_SIZE, CELL_SIZE),
                border_radius=5
            )

            # vẽ mắt rắn
            if i == 0:
               x, y = segment
               pygame.draw.circle(
                   screen,
                   WHITE,
                   (x + 6, y + 6),
                   2
                )
               pygame.draw.circle(
                   screen,
                   WHITE,
                   (x + 14, y + 6),
                   2
                )
               pygame.draw.circle(
                   screen,
                   BLACK,
                   (x + 6, y + 6),
                   1
                )
               pygame.draw.circle(
                   screen,
                   BLACK,
                   (x + 14, y + 6),
                   1
                )

        # điểm số
        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )
        screen.blit(score_text, (10, 10))

        if difficulty == 1:
            mode_name = "Easy"
        elif difficulty == 2:
            mode_name = "Medium"
        else:
            mode_name = "Hard"
        mode_text = font.render(
            f"Mode: {mode_name}",
            True,
            WHITE
        )
        screen.blit(mode_text, (10, 50))
        skin_text = font.render(
            f"Skin Lv: {skin_level}",
            True,
            WHITE
        )
        screen.blit(
            skin_text,
            (10, 90)
        )

def draw_game_over():
    screen.fill(BLACK)
    game_over_text = big_font.render(
        "Game Over!",
        True,
        RED
    )
    restart_text = font.render(
        "Press R To Restart",
        True,
        WHITE
    )
    menu_text = font.render(
        "Press M For Main Menu",
        True,
        WHITE
    )
    screen.blit(
        game_over_text,
        (
            WIDTH // 2 - game_over_text.get_width() // 2,
            180
        )
    )
    screen.blit(
        restart_text,
        (
            WIDTH // 2 - restart_text.get_width() // 2,
            280
        )
    )
    screen.blit(
        menu_text,
        (
            WIDTH // 2 - menu_text.get_width() // 2,
            330
        )
    )

snake, direction, food, score = reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_state == MAIN_MENU:
                if event.key == pygame.K_RETURN:
                    game_state = DIFFICULTY_MENU
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()    
            elif game_state == DIFFICULTY_MENU:
                if event.key == pygame.K_1:
                    set_difficulty(1)
                    snake, direction, food, score = reset_game()
                    game_state = PLAYING
                elif event.key == pygame.K_2:
                    set_difficulty(2)
                    snake, direction, food, score = reset_game()
                    game_state = PLAYING
                elif event.key == pygame.K_3:
                    set_difficulty(3)
                    snake, direction, food, score = reset_game()
                    game_state = PLAYING
            elif game_state == PLAYING:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)   
            elif game_state == GAME_OVER:
                if event.key == pygame.K_r:
                    snake, direction, food, score = reset_game()
                    game_state = PLAYING
                elif event.key == pygame.K_m:
                    game_state = MAIN_MENU              

    if game_state == PLAYING:
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        if (
            new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        ):
            game_state = GAME_OVER

        elif new_head in snake:    
            game_state = GAME_OVER
        else:
            snake.insert(0, new_head)

            # ăn mồi
            global level_message, message_timer
            if new_head == food:
                score += score_per_food
                update_skin()
                if score >= 10:
                    level_message = "Dragon evolved to Fire Form!"
                    message_timer = 180
                elif score >= 20:
                    level_message = "Dragon evolved to Gold Form!"
                    message_timer = 180
                elif score >= 30:
                    level_message = "Dragon evolved to Shadow Form!"
                    message_timer = 180
                elif score >= 40:
                    level_message = "Dragon evolved to Rainbow Dragon!"
                    message_timer = 180 
                food = create_food(snake)
            else:
                snake.pop()

    # vẽ màn hình
    if game_state == MAIN_MENU:
        draw_main_menu()
    elif game_state == DIFFICULTY_MENU:
        draw_difficulty_menu()
    elif game_state == PLAYING:
        screen.fill(BLACK)
        draw_grid()
        draw_game()
    elif game_state == GAME_OVER:
        screen.fill(BLACK)
        draw_grid()
        draw_game()
        draw_game_over()
    
    pygame.display.flip()
    clock.tick(snake_speed)