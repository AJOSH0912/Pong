import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Ball dimensions
BALL_SIZE = 20

# Paddle speed
PADDLE_SPEED = 7

# Ball speed
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
BALL_SPEED_INCREMENT = 0.1  # Speed increment for the ball

# Create paddles
left_paddle = pygame.Rect(10, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 20, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)

# Create ball
ball = pygame.Rect((SCREEN_WIDTH // 2) - (BALL_SIZE // 2), (SCREEN_HEIGHT // 2) - (BALL_SIZE // 2), BALL_SIZE, BALL_SIZE)

# Paddle movement variables
left_paddle_speed = 0
right_paddle_speed = 0

# Clock to manage ball speed increment
clock = pygame.time.Clock()
time_elapsed_since_last_speed_increase = 0
SPEED_INCREASE_INTERVAL = 2000  # Speed increase interval in milliseconds

#Game mode variable
game_mode = None

#AI Paddle speed
AI_SPEED = 5

def show_menu():
    """Display the menu to choose game mode."""
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Pong Game", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))

    font = pygame.font.Font(None, 36)
    text1 = font.render("1. Single Player", True, WHITE)
    text2 = font.render("2. Two Player", True, WHITE)
    screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

    pygame.display.flip()
    
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keydown events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                left_paddle_speed = -PADDLE_SPEED
            elif event.key == pygame.K_s:
                left_paddle_speed = PADDLE_SPEED
            elif event.key == pygame.K_UP:
                right_paddle_speed = -PADDLE_SPEED
            elif event.key == pygame.K_DOWN:
                right_paddle_speed = PADDLE_SPEED
        # Keyup events
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                left_paddle_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                right_paddle_speed = 0
    
    # Move paddles
    left_paddle.y += left_paddle_speed
    right_paddle.y += right_paddle_speed

    # Prevent paddles from moving out of the screen
    if left_paddle.top < 0:
        left_paddle.top = 0
    if left_paddle.bottom > SCREEN_HEIGHT:
        left_paddle.bottom = SCREEN_HEIGHT
    if right_paddle.top < 0:
        right_paddle.top = 0
    if right_paddle.bottom > SCREEN_HEIGHT:
        right_paddle.bottom = SCREEN_HEIGHT

    # Move ball
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Ball collision with top/bottom walls
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        BALL_SPEED_Y = -BALL_SPEED_Y

# Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        BALL_SPEED_X = -BALL_SPEED_X

    # Ball goes out of bounds
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball.x = (SCREEN_WIDTH // 2) - (BALL_SIZE // 2)
        ball.y = (SCREEN_HEIGHT // 2) - (BALL_SIZE // 2)
        BALL_SPEED_X = -BALL_SPEED_X
        #Reset ball speed
        BALL_SPEED_X = 5
        BALL_SPEED_Y = 5

    # New: Increase ball speed over time
    time_elapsed_since_last_speed_increase += clock.get_time()
    if time_elapsed_since_last_speed_increase >= SPEED_INCREASE_INTERVAL:
        BALL_SPEED_X *= 1 + BALL_SPEED_INCREMENT
        BALL_SPEED_Y *= 1 + BALL_SPEED_INCREMENT
        time_elapsed_since_last_speed_increase = 0
    # Clear screen
    screen.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)

    # Draw ball
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw center line
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)
