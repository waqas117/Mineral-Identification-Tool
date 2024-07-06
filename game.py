import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Snake and food size
BLOCK_SIZE = 20

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

def draw_snake(snake_list):
    for i, block in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Head
            pygame.draw.rect(screen, YELLOW, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])
            eye_radius = BLOCK_SIZE // 5
            pygame.draw.circle(screen, BLACK, (block[0] + BLOCK_SIZE // 4, block[1] + BLOCK_SIZE // 4), eye_radius)
            pygame.draw.circle(screen, BLACK, (block[0] + 3 * BLOCK_SIZE // 4, block[1] + BLOCK_SIZE // 4), eye_radius)
        else:  # Body
            pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def draw_food(foodx, foody):
    pygame.draw.circle(screen, RED, (foodx + BLOCK_SIZE // 2, foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2)

def display_score(score):
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [10, 10])

def message(msg, color, y_displace=0):
    font = pygame.font.SysFont(None, 50)
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + y_displace))
    screen.blit(text, text_rect)

def game_intro():
    intro = True
    while intro:
        screen.fill(BLACK)
        message("Welcome to Snake", GREEN, -50)
        message("Press P to Play or Q to Quit", WHITE, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return True
                if event.key == pygame.K_q:
                    return False

def game_loop():
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    score = 0

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("Game Over!", RED, -50)
            message(f"Final Score: {score}", WHITE, 0)
            message("Press P to Play Again or Q to Quit", WHITE, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        draw_food(foodx, foody)
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        display_score(score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            length_of_snake += 1
            score += 10

        clock.tick(15)

    return False

def main():
    while True:
        if game_intro():
            if not game_loop():
                break
        else:
            break

    pygame.quit()

if __name__ == "__main__":
    main()