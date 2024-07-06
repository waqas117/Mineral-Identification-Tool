import pygame
import random
import json
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Snake and food size
BLOCK_SIZE = 20

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Enhanced Snake Game')

clock = pygame.time.Clock()

# Load images
try:
    background_img = pygame.image.load('background.png')
    food_img = pygame.image.load('food.png')
    power_up_img = pygame.image.load('power_up.png')

    # Resize images
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    food_img = pygame.transform.scale(food_img, (BLOCK_SIZE, BLOCK_SIZE))
    power_up_img = pygame.transform.scale(power_up_img, (BLOCK_SIZE, BLOCK_SIZE))
except pygame.error:
    print("Warning: Unable to load one or more images. Using colored rectangles instead.")
    background_img = food_img = power_up_img = None

# Load sounds
try:
    eat_sound = pygame.mixer.Sound('eat.wav')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
except pygame.error:
    print("Warning: Unable to load one or more sound files. Game will run without sound.")
    eat_sound = game_over_sound = None

# Load high scores
def load_high_scores():
    if os.path.exists('high_scores.json'):
        with open('high_scores.json', 'r') as f:
            return json.load(f)
    return {'easy': 0, 'medium': 0, 'hard': 0}

# Save high scores
def save_high_scores(high_scores):
    with open('high_scores.json', 'w') as f:
        json.dump(high_scores, f)

high_scores = load_high_scores()

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
    if food_img:
        screen.blit(food_img, (foodx, foody))
    else:
        pygame.draw.rect(screen, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

def draw_power_up(power_up):
    if power_up:
        if power_up_img:
            screen.blit(power_up_img, (power_up[0], power_up[1]))
        else:
            pygame.draw.rect(screen, BLUE, [power_up[0], power_up[1], BLOCK_SIZE, BLOCK_SIZE])

def display_score(score, high_score):
    font = pygame.font.Font(None, 35)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, [10, 10])
    screen.blit(high_score_text, [10, 50])

def message(msg, color, y_displace=0, size=50):
    font = pygame.font.Font(None, size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + y_displace))
    screen.blit(text, text_rect)

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.Font(None, 30)
    textSurf = smallText.render(msg, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

def game_intro():
    intro = True
    difficulty = 'medium'
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(BLACK)
        message("Welcome to Snake", GREEN, -100, 70)
        message("Select Difficulty:", WHITE, -20)

        button("Easy", 150, 350, 100, 50, GREEN, BLUE, lambda: set_difficulty('easy'))
        button("Medium", 350, 350, 100, 50, YELLOW, BLUE, lambda: set_difficulty('medium'))
        button("Hard", 550, 350, 100, 50, RED, BLUE, lambda: set_difficulty('hard'))
        
        button("Play", 300, 450, 200, 50, GREEN, BLUE, lambda: start_game(difficulty))
        button("Quit", 300, 520, 200, 50, RED, BLUE, pygame.quit)

        message(f"Current: {difficulty.capitalize()}", YELLOW, 150, 30)
        
        pygame.display.update()
        clock.tick(15)

    return difficulty

def set_difficulty(diff):
    global difficulty
    difficulty = diff

def start_game(difficulty):
    global game_loop
    game_loop(difficulty)

def game_loop(difficulty):
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

    power_up = None
    power_up_timer = 0
    speed_boost = False
    speed_boost_timer = 0

    score = 0

    if difficulty == 'easy':
        speed = 10
    elif difficulty == 'medium':
        speed = 15
    else:  # hard
        speed = 20

    while not game_over:

        while game_close:
            if background_img:
                screen.blit(background_img, (0, 0))
            else:
                screen.fill(BLACK)
            message("Game Over!", RED, -50)
            message(f"Final Score: {score}", WHITE, 0)
            message("Press P to Play Again or Q to Quit", WHITE, 50)
            pygame.display.update()

            if score > high_scores[difficulty]:
                high_scores[difficulty] = score
                save_high_scores(high_scores)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        game_loop(difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
            if game_over_sound:
                game_over_sound.play()

        x1 += x1_change
        y1 += y1_change
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(BLACK)
        draw_food(foodx, foody)
        draw_power_up(power_up)
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True
                if game_over_sound:
                    game_over_sound.play()

        draw_snake(snake_list)
        display_score(score, high_scores[difficulty])
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            length_of_snake += 1
            score += 10
            if eat_sound:
                eat_sound.play()

            # Spawn power-up
            if random.random() < 0.3 and not power_up:  # 30% chance to spawn power-up
                power_up = [round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
                            round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE]
                power_up_timer = 50  # Power-up disappears after 50 frames

        # Handle power-up
        if power_up:
            power_up_timer -= 1
            if power_up_timer <= 0:
                power_up = None
            elif x1 == power_up[0] and y1 == power_up[1]:
                speed_boost = True
                speed_boost_timer = 30  # Speed boost lasts for 30 frames
                power_up = None

        # Handle speed boost
        if speed_boost:
            speed_boost_timer -= 1
            if speed_boost_timer <= 0:
                speed_boost = False

        clock.tick(speed + (10 if speed_boost else 0))

def main():
    while True:
        difficulty = game_intro()
        game_loop(difficulty)

if __name__ == "__main__":
    main()