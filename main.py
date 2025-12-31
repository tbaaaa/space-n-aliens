import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Space N Aliens")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 8

# Bullet
bullet_width = 5
bullet_height = 10
bullet_speed = 35
bullets = []

# Enemy
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []
enemy_spawn_rate = 45  # frames

# Score
score = 0
font = pygame.font.Font(None, 36)

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
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH = event.w
            SCREEN_HEIGHT = event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'title':
            start_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 20, 100, 40)
            exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 30, 100, 40)
            if start_button.collidepoint(event.pos):
                reset_game()
                game_state = 'playing'
            elif exit_button.collidepoint(event.pos):
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'game_over':
            if button_rect.collidepoint(event.pos):
                reset_game()
                game_state = 'playing'
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'paused':
            resume_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 30, 160, 40)
            back_button = pygame.Rect(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 20, 180, 40)
            exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 70, 180, 40)
            if resume_button.collidepoint(event.pos):
                game_state = 'playing'
            elif back_button.collidepoint(event.pos):
                game_state = 'title'
            elif exit_button.collidepoint(event.pos):
                running = False

    if game_state == 'title':
        # Define buttons
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 20, 100, 40)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 30, 100, 40)
        # Draw title
        title_text = font.render("Space N Aliens", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 80))
        # Draw start button
        pygame.draw.rect(screen, GREEN, start_button)
        start_text = font.render("Start", True, BLACK)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 10))
        # Draw exit button
        pygame.draw.rect(screen, RED, exit_button)
        exit_text = font.render("Exit", True, BLACK)
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 + 40))

    elif game_state == 'playing':
        # Player movement
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_w] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_s] and player_y < SCREEN_HEIGHT - player_height:
            player_y += player_speed
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] and frame_count % 15 == 0:  # LMB
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player_center_x = player_x + player_width // 2
            player_center_y = player_y + player_height // 2
            dx = mouse_x - player_center_x
            dy = mouse_y - player_center_y
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                dx /= distance
                dy /= distance
                bullet_vx = dx * bullet_speed
                bullet_vy = dy * bullet_speed
                bullets.append([player_center_x - bullet_width // 2, player_center_y - bullet_height // 2, bullet_vx, bullet_vy])

        # Draw player
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

        # Draw aiming line
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2
        pygame.draw.line(screen, RED, (player_center_x, player_center_y), (mouse_x, mouse_y), 2)

        # Update bullets
        for bullet in bullets[:]:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            if bullet[0] < -bullet_width or bullet[0] > SCREEN_WIDTH or bullet[1] < -bullet_height or bullet[1] > SCREEN_HEIGHT:
                bullets.remove(bullet)
            else:
                pygame.draw.line(screen, WHITE, (bullet[0], bullet[1]), (bullet[0] + bullet[2] * 3, bullet[1] + bullet[3] * 3), 3)

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

        # Check for pause
        if keys[pygame.K_ESCAPE]:
            game_state = 'paused'

    elif game_state == 'game_over':
        # Draw game over
        game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        # Draw button
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 50)
        pygame.draw.rect(screen, GREEN, button_rect)
        retry_text = font.render("Retry", True, BLACK)
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 + 10))

    elif game_state == 'paused':
        # Draw paused menu
        pause_text = font.render("Paused", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 80))
        # Define buttons
        resume_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 30, 160, 40)
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 20, 180, 40)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 70, 180, 40)
        # Draw buttons
        pygame.draw.rect(screen, GREEN, resume_button)
        resume_text = font.render("Resume", True, BLACK)
        screen.blit(resume_text, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 20))
        pygame.draw.rect(screen, BLUE, back_button)
        back_text = font.render("Back to Title", True, BLACK)
        screen.blit(back_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 30))
        pygame.draw.rect(screen, RED, exit_button)
        exit_text = font.render("Exit", True, BLACK)
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 + 80))

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

pygame.quit()