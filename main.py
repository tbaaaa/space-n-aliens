import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space N Aliens")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

# Bullet
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemy
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []
enemy_spawn_rate = 30  # frames

# Score
score = 0
font = pygame.font.Font(None, 36)

# Button
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 50)

# Game state
game_state = 'title'

# Clock
clock = pygame.time.Clock()
FPS = 60

def reset_game():
    global player_x, bullets, enemies, score, frame_count
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    bullets = []
    enemies = []
    score = 0
    frame_count = 0

# Game loop
running = True
frame_count = 0
while running:
    screen.fill(BLACK)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'game_over':
            if button_rect.collidepoint(event.pos):
                reset_game()
                game_state = 'playing'

    if game_state == 'title':
        # Draw title
        title_text = font.render("Space N Aliens", True, WHITE)
        start_text = font.render("Press Space to Start", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
        if keys[pygame.K_SPACE]:
            reset_game()
            game_state = 'playing'

    elif game_state == 'playing':
        # Player movement
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE] and frame_count % 10 == 0:  # Limit shooting rate
            bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])

        # Draw player
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

        # Update bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
            else:
                pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))

        # Spawn enemies
        if frame_count % enemy_spawn_rate == 0:
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemies.append([enemy_x, 0])

        # Update enemies
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            if enemy[1] > SCREEN_HEIGHT:
                game_state = 'game_over'
            else:
                pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

        # Check collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (bullet[0] < enemy[0] + enemy_width and
                    bullet[0] + bullet_width > enemy[0] and
                    bullet[1] < enemy[1] + enemy_height and
                    bullet[1] + bullet_height > enemy[1]):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    elif game_state == 'game_over':
        # Draw game over
        game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        # Draw button
        pygame.draw.rect(screen, GREEN, button_rect)
        retry_text = font.render("Retry", True, BLACK)
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 + 10))

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

pygame.quit()