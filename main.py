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

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
running = True
frame_count = 0
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
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
            enemies.remove(enemy)  # Game over if enemy reaches bottom
            running = False
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

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

# Game over
screen.fill(BLACK)
game_over_text = font.render("Game Over! Final Score: " + str(score), True, WHITE)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()