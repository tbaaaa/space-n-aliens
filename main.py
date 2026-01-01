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
PURPLE = (128, 0, 128)
DARK_PURPLE = (80, 0, 80)
YELLOW = (255, 255, 0)

# Difficulty tuning
LEVEL_SIZE = 30  # points per difficulty step

# Player
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 6
player_hp = 3
invincible = False
invincible_timer = 0
invincible_duration = 120  # frames (2 seconds at 60 FPS)

# Bullet
bullet_width = 5
bullet_height = 10
bullet_speed = 25
bullets = []

# Enemy
enemy_width = 50
enemy_height = 50
enemy_speed = 2
enemies = []
enemy_spawn_rate = 55  # frames
enemy_bullets = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game state
game_state = 'title'

# Clock
clock = pygame.time.Clock()
FPS = 60

def reset_game():
    global player_x, bullets, enemies, enemy_bullets, score, frame_count, player_hp, invincible, invincible_timer
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    bullets = []
    enemies = []
    enemy_bullets = []
    score = 0
    frame_count = 0
    player_hp = 3
    invincible = False
    invincible_timer = 0

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
            retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 30, 120, 40)
            back_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 20, 160, 40)
            exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 70, 120, 40)
            if retry_button.collidepoint(event.pos):
                reset_game()
                game_state = 'playing'
            elif back_button.collidepoint(event.pos):
                game_state = 'title'
            elif exit_button.collidepoint(event.pos):
                running = False
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

    elif game_state == 'playing' or game_state == 'paused':
        # Dynamic difficulty based on score
        difficulty_level = score // LEVEL_SIZE
        current_player_speed = player_speed + min(0.5 * difficulty_level, 5)
        current_bullet_speed = bullet_speed + min(3 * difficulty_level, 20)
        fire_interval = max(6, 24 - difficulty_level * 2)
        current_enemy_speed = enemy_speed + min(0.5 * difficulty_level, 6)
        current_spawn_rate = max(12, enemy_spawn_rate - difficulty_level * 2)
        current_enemy_bullet_speed = 6 + min(0.5 * difficulty_level, 6)
        # Player movement (only when not paused)
        if game_state == 'playing':
            if keys[pygame.K_a] and player_x > 0:
                player_x -= current_player_speed
            if keys[pygame.K_d] and player_x < SCREEN_WIDTH - player_width:
                player_x += current_player_speed
            if keys[pygame.K_w] and player_y > 0:
                player_y -= current_player_speed
            if keys[pygame.K_s] and player_y < SCREEN_HEIGHT - player_height:
                player_y += current_player_speed
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0] and frame_count % fire_interval == 0:  # LMB
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player_center_x = player_x + player_width // 2
                player_center_y = player_y + player_height // 2
                dx = mouse_x - player_center_x
                dy = mouse_y - player_center_y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > 0:
                    dx /= distance
                    dy /= distance
                    bullet_vx = dx * current_bullet_speed
                    bullet_vy = dy * current_bullet_speed
                    bullets.append([player_center_x - bullet_width // 2, player_center_y - bullet_height // 2, bullet_vx, bullet_vy])

        # Draw player (with flashing effect during invincibility)
        if not invincible or (invincible_timer // 10) % 2 == 0:  # Flash every 10 frames
            # Choose color based on HP
            if player_hp == 3:
                player_color = GREEN
            elif player_hp == 2:
                player_color = YELLOW
            else:  # player_hp == 1
                player_color = RED
            pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

        # Draw aiming line (only when playing)
        if game_state == 'playing':
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player_center_x = player_x + player_width // 2
            player_center_y = player_y + player_height // 2
            pygame.draw.line(screen, RED, (player_center_x, player_center_y), (mouse_x, mouse_y), 2)

        # Draw bullets
        for bullet in bullets[:]:
            pygame.draw.line(screen, WHITE, (bullet[0], bullet[1]), (bullet[0] + bullet[2] * 3, bullet[1] + bullet[3] * 3), 3)

        # Draw enemies
        for enemy in enemies[:]:
            enemy_color = PURPLE
            if enemy['type'] == 'shooter' and enemy.get('warning_timer', 0) > 0:
                # Flash dark purple every 5 frames
                if (enemy['warning_timer'] // 5) % 2 == 0:
                    enemy_color = DARK_PURPLE
            pygame.draw.rect(screen, enemy_color, (enemy['x'], enemy['y'], enemy_width, enemy_height))

        # Draw enemy bullets
        for eb in enemy_bullets[:]:
            pygame.draw.circle(screen, RED, (int(eb[0]), int(eb[1])), 5)

        # Update game state (only when playing)
        if game_state == 'playing':
            # Update bullets
            for bullet in bullets[:]:
                bullet[0] += bullet[2]
                bullet[1] += bullet[3]
                if bullet[0] < -bullet_width or bullet[0] > SCREEN_WIDTH or bullet[1] < -bullet_height or bullet[1] > SCREEN_HEIGHT:
                    bullets.remove(bullet)

            # Spawn enemies
            if frame_count % current_spawn_rate == 0:
                # Keep sine/zigzag spawns within horizontal bounds
                max_amplitude = max(20, (SCREEN_WIDTH - enemy_width) // 2)
                chosen_amplitude = min(random.randint(40, 120), max_amplitude)
                spawn_x_min = chosen_amplitude
                spawn_x_max = SCREEN_WIDTH - enemy_width - chosen_amplitude
                if spawn_x_max < spawn_x_min:
                    spawn_x_min = 0
                    spawn_x_max = SCREEN_WIDTH - enemy_width
                    chosen_amplitude = max_amplitude

                enemy_x = random.randint(spawn_x_min, spawn_x_max)

                # Movement types unlock after score 50
                if score < 50:
                    enemy_type = 'straight'
                else:
                    if difficulty_level >= 4:
                        enemy_type = random.choice(['shooter', 'sine', 'zigzag', 'straight'])
                    elif difficulty_level >= 2:
                        enemy_type = random.choice(['sine', 'zigzag', 'straight'])
                    elif difficulty_level >= 1:
                        enemy_type = random.choice(['straight', 'sine'])
                    else:
                        enemy_type = 'straight'

                new_enemy = {
                    'x': enemy_x,
                    'y': 0,
                    'base_x': enemy_x,
                    'type': enemy_type,
                    'vx': random.choice([-1, 1]) * (1.5 + 0.2 * difficulty_level),
                    'amplitude': chosen_amplitude,
                    'spawn_frame': frame_count,
                    'shoot_cooldown': 0,
                    'warning_timer': 0
                }
                if enemy_type == 'shooter':
                    base_cooldown = max(45, 90 - difficulty_level * 8)
                    new_enemy['shoot_cooldown'] = random.randint(base_cooldown, base_cooldown + 40)
                enemies.append(new_enemy)

            # Update enemies
            for enemy in enemies[:]:
                if enemy['type'] == 'sine':
                    offset = enemy['amplitude'] * math.sin((frame_count - enemy['spawn_frame']) / 25)
                    enemy['x'] = enemy['base_x'] + offset
                    enemy['x'] = max(0, min(enemy['x'], SCREEN_WIDTH - enemy_width))
                elif enemy['type'] in ('zigzag', 'shooter'):
                    enemy['x'] += enemy['vx']
                    if enemy['x'] < 0 or enemy['x'] > SCREEN_WIDTH - enemy_width:
                        enemy['vx'] *= -1
                        enemy['x'] = max(0, min(enemy['x'], SCREEN_WIDTH - enemy_width))

                enemy['y'] += current_enemy_speed

                if enemy['type'] == 'shooter':
                    warning_duration = 30
                    enemy['shoot_cooldown'] -= 1

                    # Start warning when cooldown is close to firing
                    if enemy['shoot_cooldown'] <= warning_duration and enemy.get('warning_timer', 0) == 0:
                        enemy['warning_timer'] = warning_duration

                    if enemy.get('warning_timer', 0) > 0:
                        enemy['warning_timer'] -= 1
                        if enemy['warning_timer'] <= 0 and enemy['shoot_cooldown'] <= 0:
                            player_center_x = player_x + player_width // 2
                            player_center_y = player_y + player_height // 2
                            enemy_center_x = enemy['x'] + enemy_width // 2
                            enemy_center_y = enemy['y'] + enemy_height // 2
                            dx = player_center_x - enemy_center_x
                            dy = player_center_y - enemy_center_y
                            dist = math.hypot(dx, dy)
                            if dist == 0:
                                dist = 1
                            vx = (dx / dist) * current_enemy_bullet_speed
                            vy = (dy / dist) * current_enemy_bullet_speed
                            enemy_bullets.append([enemy_center_x, enemy_center_y, vx, vy])
                            base_cooldown = max(45, 90 - difficulty_level * 8)
                            enemy['shoot_cooldown'] = random.randint(base_cooldown, base_cooldown + 40)
                            enemy['warning_timer'] = 0
                    elif enemy['shoot_cooldown'] <= 0:
                        # Failsafe: if warning was skipped, still fire
                        player_center_x = player_x + player_width // 2
                        player_center_y = player_y + player_height // 2
                        enemy_center_x = enemy['x'] + enemy_width // 2
                        enemy_center_y = enemy['y'] + enemy_height // 2
                        dx = player_center_x - enemy_center_x
                        dy = player_center_y - enemy_center_y
                        dist = math.hypot(dx, dy)
                        if dist == 0:
                            dist = 1
                        vx = (dx / dist) * current_enemy_bullet_speed
                        vy = (dy / dist) * current_enemy_bullet_speed
                        enemy_bullets.append([enemy_center_x, enemy_center_y, vx, vy])
                        base_cooldown = max(45, 90 - difficulty_level * 8)
                        enemy['shoot_cooldown'] = random.randint(base_cooldown, base_cooldown + 40)
                        enemy['warning_timer'] = 0

                if enemy['y'] > SCREEN_HEIGHT:
                    enemies.remove(enemy)
                    if not invincible:
                        player_hp -= 1
                        if player_hp <= 0:
                            game_state = 'game_over'
                        else:
                            invincible = True
                            invincible_timer = invincible_duration
                    continue

            # Update enemy bullets
            for eb in enemy_bullets[:]:
                eb[0] += eb[2]
                eb[1] += eb[3]
                if eb[0] < -10 or eb[0] > SCREEN_WIDTH + 10 or eb[1] < -10 or eb[1] > SCREEN_HEIGHT + 10:
                    enemy_bullets.remove(eb)

            # Check bullet-enemy collisions
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if (bullet[0] < enemy['x'] + enemy_width and
                        bullet[0] + bullet_width > enemy['x'] and
                        bullet[1] < enemy['y'] + enemy_height and
                        bullet[1] + bullet_height > enemy['y']):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 1
                        break

            # Check player-enemy collisions
            if not invincible:
                for enemy in enemies[:]:
                    if (player_x < enemy['x'] + enemy_width and
                        player_x + player_width > enemy['x'] and
                        player_y < enemy['y'] + enemy_height and
                        player_y + player_height > enemy['y']):
                        enemies.remove(enemy)
                        player_hp -= 1
                        if player_hp <= 0:
                            game_state = 'game_over'
                        else:
                            invincible = True
                            invincible_timer = invincible_duration
                        break

            # Check player hit by enemy bullets
            if not invincible:
                for eb in enemy_bullets[:]:
                    if (player_x < eb[0] + 6 and
                        player_x + player_width > eb[0] - 6 and
                        player_y < eb[1] + 6 and
                        player_y + player_height > eb[1] - 6):
                        enemy_bullets.remove(eb)
                        player_hp -= 1
                        if player_hp <= 0:
                            game_state = 'game_over'
                        else:
                            invincible = True
                            invincible_timer = invincible_duration
                        break

            # Update invincibility timer
            if invincible:
                invincible_timer -= 1
                if invincible_timer <= 0:
                    invincible = False

        # Draw score and HP
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        hp_text = font.render(f"HP: {player_hp}", True, WHITE)
        screen.blit(hp_text, (10, 50))

        # Check for pause (only when playing)
        if game_state == 'playing' and keys[pygame.K_ESCAPE]:
            game_state = 'paused'

        # Draw pause overlay if paused
        if game_state == 'paused':
            # Draw semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            # Draw paused menu
            pause_text = font.render("Paused", True, WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 80))
            # Define buttons
            resume_button = pygame.Rect(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 30, 180, 40)
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

    elif game_state == 'game_over':
        # Draw game over
        game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 80))
        # Define buttons
        retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 30, 120, 40)
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 20, 160, 40)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 70, 120, 40)
        # Draw buttons
        pygame.draw.rect(screen, GREEN, retry_button)
        retry_text = font.render("Retry", True, BLACK)
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 20))
        pygame.draw.rect(screen, BLUE, back_button)
        back_text = font.render("Back to Title", True, BLACK)
        screen.blit(back_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 30))
        pygame.draw.rect(screen, RED, exit_button)
        exit_text = font.render("Exit", True, BLACK)
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 + 80))

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

pygame.quit()