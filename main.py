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
CYAN = (0, 255, 255)
ORANGE = (255, 140, 0)

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

# Boss
boss = None
boss_spawn_threshold = 100
reflectable_projectiles = []
score = 190

# Final boss hazards
swarm_minions = []  # kamikaze crash minions
grabbers = []       # latch-on minions
multiplying_bullets = []  # bouncing, splitting bullets
exploding_bullets = []    # timed explosives
laser_warnings = []       # telegraphed lasers before firing
active_lasers = []        # active laser beams
path_hazards = []         # winding corridor hazards

# Grab state
grabbed = False
grab_escape_meter = 0
grab_escape_target = 25
font = pygame.font.Font(None, 36)

# Game state
game_state = 'title'

# Clock
clock = pygame.time.Clock()
FPS = 60

def reset_game():
    global player_x, bullets, enemies, enemy_bullets, boss, reflectable_projectiles, score, frame_count, player_hp, invincible, invincible_timer, boss_spawn_threshold, swarm_minions, grabbers, multiplying_bullets, exploding_bullets, laser_warnings, active_lasers, path_hazards, grabbed, grab_escape_meter
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    bullets = []
    enemies = []
    enemy_bullets = []
    boss = None
    reflectable_projectiles = []
    swarm_minions = []
    grabbers = []
    multiplying_bullets = []
    exploding_bullets = []
    laser_warnings = []
    active_lasers = []
    path_hazards = []
    boss_spawn_threshold = 100
    score = 190
    frame_count = 0
    player_hp = 3
    invincible = False
    invincible_timer = 0
    grabbed = False
    grab_escape_meter = 0

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
        # Milestone-based difficulty progression
        if score < 50:
            current_player_speed = player_speed
            current_bullet_speed = bullet_speed
            fire_interval = 24
            current_enemy_speed = enemy_speed
            current_spawn_rate = enemy_spawn_rate
            current_enemy_bullet_speed = 6
        elif score < 100:
            current_player_speed = player_speed + 0.5
            current_bullet_speed = bullet_speed + 2
            fire_interval = 22
            current_enemy_speed = enemy_speed + 0.3
            current_spawn_rate = enemy_spawn_rate - 2
            current_enemy_bullet_speed = 6.5
        elif score < 150:
            current_player_speed = player_speed + 1.2
            current_bullet_speed = bullet_speed + 5
            fire_interval = 18
            current_enemy_speed = enemy_speed + 0.7
            current_spawn_rate = max(12, enemy_spawn_rate - 5)
            current_enemy_bullet_speed = 7.5
        elif score < 200:
            current_player_speed = player_speed + 2.0
            current_bullet_speed = bullet_speed + 9
            fire_interval = 14
            current_enemy_speed = enemy_speed + 1.2
            current_spawn_rate = max(12, enemy_spawn_rate - 8)
            current_enemy_bullet_speed = 8.5
        else:  # score >= 200
            current_player_speed = player_speed + 3.0
            current_bullet_speed = bullet_speed + 12
            fire_interval = 10
            current_enemy_speed = enemy_speed + 1.8
            current_spawn_rate = max(12, enemy_spawn_rate - 12)
            current_enemy_bullet_speed = 9.5
        # Player movement (only when not paused)
        if game_state == 'playing':
            if not grabbed:
                if keys[pygame.K_a] and player_x > 0:
                    player_x -= current_player_speed
                if keys[pygame.K_d] and player_x < SCREEN_WIDTH - player_width:
                    player_x += current_player_speed
                if keys[pygame.K_w] and player_y > 0:
                    player_y -= current_player_speed
                if keys[pygame.K_s] and player_y < SCREEN_HEIGHT - player_height:
                    player_y += current_player_speed
            else:
                # Struggle mechanic when grabbed
                grab_escape_meter = max(0, grab_escape_meter - 0.2)
                if keys[pygame.K_a] or keys[pygame.K_d]:
                    grab_escape_meter += 1
                grab_escape_meter = max(0, min(grab_escape_meter, grab_escape_target))
                if grab_escape_meter >= grab_escape_target:
                    grabbed = False
                    grab_escape_meter = 0
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

        # Draw boss if active
        if boss:
            # Boss flashes cyan when vulnerable
            if boss.get('vulnerable', False):
                boss_color = CYAN
            else:
                boss_color = BLUE
            
            if boss.get('type') == 'star':
                # Draw star boss with square hole
                center_x = boss['x'] + boss['width'] // 2
                center_y = boss['y'] + boss['height'] // 2
                outer_radius = boss['width'] // 2
                inner_radius = outer_radius // 3
                
                # Draw star points
                points = []
                for i in range(8):
                    angle = i * (360 / 8)
                    radius = outer_radius if i % 2 == 0 else inner_radius * 1.5
                    rad = math.radians(angle - 90)
                    x = center_x + radius * math.cos(rad)
                    y = center_y + radius * math.sin(rad)
                    points.append((x, y))
                pygame.draw.polygon(screen, boss_color, points)
                
                # Draw square hole in middle
                hole_size = inner_radius
                pygame.draw.rect(screen, BLACK, (center_x - hole_size // 2, center_y - hole_size // 2, hole_size, hole_size))
            elif boss.get('type') == 'alien':
                # Stage-based palette for alien boss
                stage = boss.get('stage', 1)
                stage_colors = {
                    1: (90, 200, 255),   # cyan-ish
                    2: (120, 255, 160),  # green-ish
                    3: (255, 180, 90),   # orange-ish
                    4: (255, 80, 120)    # red-ish
                }
                head_color = stage_colors.get(stage, boss_color)
                accent_color = WHITE if stage < 3 else YELLOW
                core_color = RED if stage >= 3 else PURPLE

                center_x = boss['x'] + boss['width'] // 2
                center_y = boss['y'] + boss['height'] // 2

                # Main head
                pygame.draw.ellipse(screen, head_color, (boss['x'], boss['y'], boss['width'], boss['height']))
                # Forehead crest
                crest_points = [
                    (center_x, boss['y'] - 20),
                    (boss['x'] + 20, boss['y'] + boss['height'] // 3),
                    (boss['x'] + boss['width'] - 20, boss['y'] + boss['height'] // 3)
                ]
                pygame.draw.polygon(screen, accent_color, crest_points)
                # Eyes
                eye_w = boss['width'] // 5
                eye_h = boss['height'] // 8
                left_eye_rect = (boss['x'] + boss['width'] * 0.25 - eye_w // 2, center_y - eye_h, eye_w, eye_h)
                right_eye_rect = (boss['x'] + boss['width'] * 0.75 - eye_w // 2, center_y - eye_h, eye_w, eye_h)
                pygame.draw.ellipse(screen, BLACK, left_eye_rect)
                pygame.draw.ellipse(screen, BLACK, right_eye_rect)
                pygame.draw.circle(screen, RED, (int(left_eye_rect[0] + eye_w * 0.75), int(center_y)), 6)
                pygame.draw.circle(screen, RED, (int(right_eye_rect[0] + eye_w * 0.25), int(center_y)), 6)
                # Mouth / core
                mouth_rect = (boss['x'] + boss['width'] * 0.35, center_y + boss['height'] * 0.15, boss['width'] * 0.3, boss['height'] * 0.15)
                pygame.draw.ellipse(screen, core_color, mouth_rect)
                # Tentacles
                for i in range(5):
                    offset = i * (boss['width'] // 5)
                    start = (boss['x'] + offset + 10, boss['y'] + boss['height'])
                    end = (start[0] + ((-1) ** i) * 40, boss['y'] + boss['height'] + 60)
                    pygame.draw.line(screen, accent_color, start, end, 6)
                # Shoulder spikes per stage
                spike_span = boss['width'] // 4
                for dx in [-spike_span, 0, spike_span]:
                    spike_base = (center_x + dx, boss['y'] + boss['height'] * 0.2)
                    spike_tip = (spike_base[0], spike_base[1] - 25 - stage * 5)
                    pygame.draw.line(screen, core_color, spike_base, spike_tip, 5)
            else:
                # Regular rectangular boss
                pygame.draw.rect(screen, boss_color, (boss['x'], boss['y'], boss['width'], boss['height']))
            
            # Draw boss HP bar
            hp_ratio = boss['hp'] / boss['max_hp']
            hp_bar_width = boss['width']
            hp_bar_height = 10
            pygame.draw.rect(screen, RED, (boss['x'], boss['y'] - 20, hp_bar_width * hp_ratio, hp_bar_height))
            pygame.draw.rect(screen, WHITE, (boss['x'], boss['y'] - 20, hp_bar_width, hp_bar_height), 2)

        # Draw reflectable projectiles
        for proj in reflectable_projectiles[:]:
            # Rotate square based on rotation angle
            angle = proj['rotation']
            size = 15
            center_x, center_y = proj['x'], proj['y']
            
            # Calculate rotated corners
            corners = []
            for i in range(4):
                corner_angle = angle + i * 90
                rad = math.radians(corner_angle)
                x = center_x + size * math.cos(rad)
                y = center_y + size * math.sin(rad)
                corners.append((x, y))
            
            color = YELLOW if proj['reflected'] else PURPLE
            pygame.draw.polygon(screen, color, corners)

        # Draw crash minions
        for m in swarm_minions[:]:
            pygame.draw.polygon(screen, RED, [
                (m['x'], m['y']),
                (m['x'] - 12, m['y'] + 30),
                (m['x'] + 12, m['y'] + 30)
            ])

        # Draw grabbers (tentacle-like)
        for g in grabbers[:]:
            body_color = CYAN if not g.get('attached', False) else YELLOW
            pygame.draw.circle(screen, body_color, (int(g['x']), int(g['y'])), 14)
            pygame.draw.line(screen, PURPLE, (int(g['x']), int(g['y'])), (int(g['x']), int(g['y'] + 25)), 4)

        # Draw multiplying bouncing bullets
        for b in multiplying_bullets[:]:
            pygame.draw.circle(screen, WHITE, (int(b['x']), int(b['y'])), 6)

        # Draw exploding bullets (core + fuse ring)
        for eb in exploding_bullets[:]:
            pygame.draw.circle(screen, ORANGE, (int(eb['x']), int(eb['y'])), 7)
            # Fuse indicator (shrinks as fuse ticks)
            fuse_ratio = max(0, eb['fuse']) / eb['max_fuse']
            pygame.draw.circle(screen, YELLOW, (int(eb['x']), int(eb['y'])), max(2, int(10 * fuse_ratio)), 2)

        # Draw laser warnings and active lasers
        for lw in laser_warnings[:]:
            pygame.draw.line(screen, YELLOW, lw['start'], lw['end'], 3)
        for al in active_lasers[:]:
            pygame.draw.line(screen, RED, al['start'], al['end'], 8)

        # Draw path hazards (safe corridors in DARK_PURPLE outline)
        for path in path_hazards[:]:
            for rect in path['rects']:
                pygame.draw.rect(screen, (40, 0, 60), rect, 3)

        # Update game state (only when playing)
        if game_state == 'playing':
            # Spawn boss if score threshold is reached
            if boss is None and score >= boss_spawn_threshold and score % 100 == 0 and frame_count > 0:
                # Determine boss type based on current score
                if score == 100:
                    # First boss - rectangular
                    boss = {
                        'type': 'rect',
                        'x': SCREEN_WIDTH // 2 - 60,
                        'y': 50,
                        'width': 120,
                        'height': 120,
                        'hp': 30,
                        'max_hp': 30,
                        'attack_timer': 0,
                        'attack_pattern': 0,
                        'vx': random.choice([-1, 1]) * 1.5,
                        'vy': random.choice([-0.5, 0.5]),
                        'vulnerability_timer': 0,
                        'vulnerable': False
                    }
                elif score == 200:
                    # Second boss - star with reflectable projectiles
                    boss = {
                        'type': 'star',
                        'x': SCREEN_WIDTH // 2 - 75,
                        'y': 50,
                        'width': 150,
                        'height': 150,
                        'hp': 80,
                        'max_hp': 80,
                        'attack_timer': 0,
                        'attack_pattern': 0,
                        'vx': random.choice([-1, 1]) * 2.5,
                        'vy': random.choice([-0.8, 0.8]),
                        'vulnerability_timer': 0,
                        'vulnerable': False
                    }
                else:
                    # Final boss - alien with stages and brutal patterns
                    boss = {
                        'type': 'alien',
                        'x': SCREEN_WIDTH // 2 - 90,
                        'y': 40,
                        'width': 180,
                        'height': 180,
                        'hp': 240,
                        'max_hp': 240,
                        'attack_timer': 0,
                        'attack_pattern': 0,
                        'vx': random.choice([-1, 1]) * 3.2,
                        'vy': random.choice([-1.4, 1.4]),
                        'vulnerability_timer': 0,
                        'vulnerable': True,  # always damageable, but very tanky
                        'stage': 1,
                        'last_stage': 1,
                        'stage_change_timer': 0
                    }
                boss_spawn_threshold += 100

            # Update boss if active
            if boss:
                # Move boss
                boss['x'] += boss['vx']
                boss['y'] += boss['vy']
                
                # Keep boss within bounds and bounce
                if boss['x'] < 0 or boss['x'] > SCREEN_WIDTH - boss['width']:
                    boss['vx'] *= -1
                    boss['x'] = max(0, min(boss['x'], SCREEN_WIDTH - boss['width']))
                if boss['y'] < 0 or boss['y'] > SCREEN_HEIGHT // 2:
                    boss['vy'] *= -1
                    boss['y'] = max(0, min(boss['y'], SCREEN_HEIGHT // 2))
                
                boss['attack_timer'] += 1
                boss['vulnerability_timer'] += 1

                # Vulnerability handling
                if boss.get('type') == 'alien':
                    boss['vulnerable'] = True
                elif boss['vulnerability_timer'] % 480 < 90:
                    boss['vulnerable'] = True
                else:
                    boss['vulnerable'] = False

                # Different attack patterns based on boss type
                if boss.get('type') == 'alien':
                    # Stage calculation
                    hp_ratio = boss['hp'] / boss['max_hp'] if boss['max_hp'] > 0 else 1
                    stage = 1
                    if hp_ratio <= 0.25:
                        stage = 4
                    elif hp_ratio <= 0.5:
                        stage = 3
                    elif hp_ratio <= 0.75:
                        stage = 2
                    if stage != boss.get('stage', 1):
                        boss['stage'] = stage
                        boss['stage_change_timer'] = 0
                        # Slight speed ramp each transition
                        boss['vx'] *= 1.15
                        boss['vy'] *= 1.15
                    boss['stage_change_timer'] += 1

                    # Attack pattern selection cadence per stage
                    if boss['stage'] == 1:
                        pattern_pool = [0, 2]
                        select_every = 110
                    elif boss['stage'] == 2:
                        pattern_pool = [0, 1, 3]
                        select_every = 95
                    elif boss['stage'] == 3:
                        pattern_pool = [0, 1, 2, 3, 4]
                        select_every = 80
                    else:
                        pattern_pool = [0, 1, 2, 3, 4, 5]
                        select_every = 65

                    if boss['attack_timer'] % select_every == 0:
                        boss['attack_pattern'] = random.choice(pattern_pool)

                    boss_x = boss['x'] + boss['width'] // 2
                    boss_y = boss['y'] + boss['height'] // 2

                    # Pattern definitions
                    # 0: Swarm crash minions
                    if boss['attack_pattern'] == 0 and boss['attack_timer'] % 35 == 0:
                        for _ in range(2 + boss['stage']):
                            spawn_edge = random.choice(['left', 'right', 'top'])
                            if spawn_edge == 'top':
                                sx = random.randint(0, SCREEN_WIDTH)
                                sy = -20
                            elif spawn_edge == 'left':
                                sx = -20
                                sy = random.randint(0, SCREEN_HEIGHT // 2)
                            else:
                                sx = SCREEN_WIDTH + 20
                                sy = random.randint(0, SCREEN_HEIGHT // 2)
                            dx = player_x + player_width // 2 - sx
                            dy = player_y + player_height // 2 - sy
                            dist = math.hypot(dx, dy) or 1
                            speed = 3.5 + boss['stage'] * 0.6
                            vx = (dx / dist) * speed
                            vy = (dy / dist) * speed
                            swarm_minions.append({'x': sx, 'y': sy, 'vx': vx, 'vy': vy})

                    # 1: Grabber minion
                    elif boss['attack_pattern'] == 1 and boss['attack_timer'] % 120 == 0:
                        sx = boss_x + random.randint(-50, 50)
                        sy = boss_y
                        grabbers.append({'x': sx, 'y': sy, 'vx': 0, 'vy': 2.5 + boss['stage'] * 0.4, 'attached': False})

                    # 2: Multiplying bouncing bullets
                    elif boss['attack_pattern'] == 2 and boss['attack_timer'] % 25 == 0:
                        dx = player_x + player_width // 2 - boss_x
                        dy = player_y + player_height // 2 - boss_y
                        dist = math.hypot(dx, dy) or 1
                        speed = 6 + boss['stage'] * 0.7
                        vx = (dx / dist) * speed
                        vy = (dy / dist) * speed
                        multiplying_bullets.append({'x': boss_x, 'y': boss_y, 'vx': vx, 'vy': vy, 'split_timer': 45, 'bounces': 0, 'split_count': 0})

                    # 3: Exploding delayed shots
                    elif boss['attack_pattern'] == 3 and boss['attack_timer'] % 40 == 0:
                        dx = player_x + player_width // 2 - boss_x
                        dy = player_y + player_height // 2 - boss_y
                        dist = math.hypot(dx, dy) or 1
                        speed = 5.5 + boss['stage'] * 0.5
                        vx = (dx / dist) * speed
                        vy = (dy / dist) * speed
                        fuse = 90 - boss['stage'] * 10
                        exploding_bullets.append({'x': boss_x, 'y': boss_y, 'vx': vx, 'vy': vy, 'fuse': fuse, 'max_fuse': fuse})

                    # 4: Telegraph lasers
                    elif boss['attack_pattern'] == 4 and boss['attack_timer'] % 140 == 0:
                        orientation = random.choice(['vertical', 'diagonal'])
                        if orientation == 'vertical':
                            x_pos = random.randint(80, SCREEN_WIDTH - 80)
                            start = (x_pos, 0)
                            end = (x_pos, SCREEN_HEIGHT)
                        else:
                            start = (boss_x, boss_y)
                            end = (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT)
                        laser_warnings.append({'start': start, 'end': end, 'charge': 50})

                    # 5: Winding path hazard (stage 4 only)
                    elif boss['attack_pattern'] == 5 and boss['stage'] >= 4 and boss['attack_timer'] % 200 == 0:
                        segment_height = SCREEN_HEIGHT // 6
                        corridor_width = 160
                        x_center = random.randint(corridor_width, SCREEN_WIDTH - corridor_width)
                        new_rects = []
                        for i in range(6):
                            x_center += random.randint(-120, 120)
                            x_center = max(corridor_width, min(x_center, SCREEN_WIDTH - corridor_width))
                            rect = pygame.Rect(x_center - corridor_width // 2, i * segment_height, corridor_width, segment_height)
                            new_rects.append(rect)
                        path_hazards.append({'rects': new_rects, 'duration': 220})

                elif boss.get('type') == 'star':
                    # Star boss - shoots reflectable spinning squares and fast bullets
                    
                    # Pattern selection every 2 seconds
                    if boss['attack_timer'] % 120 == 0:
                        boss['attack_pattern'] = random.randint(0, 3)
                    
                    # Pattern 0: 8-way square burst
                    if boss['attack_pattern'] == 0 and boss['attack_timer'] % 80 == 0:
                        boss_x = boss['x'] + boss['width'] // 2
                        boss_y = boss['y'] + boss['height'] // 2
                        # Shoot 8 reflectable squares in all directions
                        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
                            rad = math.radians(angle)
                            vx = math.cos(rad) * 3.5
                            vy = math.sin(rad) * 3.5
                            reflectable_projectiles.append({
                                'x': boss_x,
                                'y': boss_y,
                                'vx': vx,
                                'vy': vy,
                                'rotation': angle,
                                'reflected': False
                            })
                    
                    # Pattern 1: Aimed fast bullets at player
                    elif boss['attack_pattern'] == 1 and boss['attack_timer'] % 20 == 0:
                        boss_x = boss['x'] + boss['width'] // 2
                        boss_y = boss['y'] + boss['height'] // 2
                        dx = player_x + player_width // 2 - boss_x
                        dy = player_y + player_height // 2 - boss_y
                        dist = math.hypot(dx, dy)
                        if dist > 0:
                            vx = (dx / dist) * 7
                            vy = (dy / dist) * 7
                            enemy_bullets.append([boss_x, boss_y, vx, vy])
                    
                    # Pattern 2: Spiral of squares
                    elif boss['attack_pattern'] == 2 and boss['attack_timer'] % 15 == 0:
                        boss_x = boss['x'] + boss['width'] // 2
                        boss_y = boss['y'] + boss['height'] // 2
                        spiral_angle = (boss['attack_timer'] * 15) % 360
                        rad = math.radians(spiral_angle)
                        vx = math.cos(rad) * 4
                        vy = math.sin(rad) * 4
                        reflectable_projectiles.append({
                            'x': boss_x,
                            'y': boss_y,
                            'vx': vx,
                            'vy': vy,
                            'rotation': spiral_angle,
                            'reflected': False
                        })
                    
                    # Pattern 3: Triple spread + squares
                    elif boss['attack_pattern'] == 3 and boss['attack_timer'] % 50 == 0:
                        boss_x = boss['x'] + boss['width'] // 2
                        boss_y = boss['y'] + boss['height'] // 2
                        # Calculate angle to player
                        dx = player_x + player_width // 2 - boss_x
                        dy = player_y + player_height // 2 - boss_y
                        base_angle = math.degrees(math.atan2(dy, dx))
                        # Fire 3 fast bullets in spread
                        for angle_offset in [-20, 0, 20]:
                            angle = base_angle + angle_offset
                            rad = math.radians(angle)
                            vx = math.cos(rad) * 6
                            vy = math.sin(rad) * 6
                            enemy_bullets.append([boss_x, boss_y, vx, vy])
                        # Also shoot 4 squares
                        for angle in [0, 90, 180, 270]:
                            rad = math.radians(angle)
                            vx = math.cos(rad) * 3
                            vy = math.sin(rad) * 3
                            reflectable_projectiles.append({
                                'x': boss_x,
                                'y': boss_y,
                                'vx': vx,
                                'vy': vy,
                                'rotation': angle,
                                'reflected': False
                            })
                else:
                    # Regular rectangular boss attacks
                    # Boss attack patterns
                    if boss['attack_timer'] % 40 == 0:
                        boss['attack_pattern'] = random.randint(0, 1)

                    # Pattern 0: Spread shot aimed at player
                    if boss['attack_pattern'] == 0 and boss['attack_timer'] % 40 == 0:
                        boss_x = boss['x'] + boss['width'] // 2
                        boss_y = boss['y'] + boss['height']
                        # Calculate angle to player
                        dx = player_x + player_width // 2 - boss_x
                        dy = player_y + player_height // 2 - boss_y
                        base_angle = math.degrees(math.atan2(dy, dx))
                        # Fire 3 shots in a spread around player direction
                        for angle_offset in [-15, 0, 15]:
                            angle = base_angle + angle_offset
                            rad = math.radians(angle)
                            vx = math.cos(rad) * 4
                            vy = math.sin(rad) * 4
                            enemy_bullets.append([boss_x, boss_y, vx, vy])
                    # Pattern 1: Aimed shot at player
                    elif boss['attack_pattern'] == 1 and boss['attack_timer'] % 50 == 0:
                        boss_x = boss['x'] + boss['width'] // 2
                        boss_y = boss['y'] + boss['height']
                        dx = player_x + player_width // 2 - boss_x
                        dy = player_y + player_height // 2 - boss_y
                        dist = math.hypot(dx, dy)
                        if dist > 0:
                            vx = (dx / dist) * 5
                            vy = (dy / dist) * 5
                            enemy_bullets.append([boss_x, boss_y, vx, vy])

            # Spawn regular enemies only if no boss
            if boss is None and frame_count % current_spawn_rate == 0:
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

                # Enemy types unlock at score milestones
                if score < 50:
                    enemy_type = 'straight'
                elif score < 100:
                    enemy_type = random.choice(['straight', 'sine'])
                elif score < 150:
                    enemy_type = random.choice(['sine', 'zigzag', 'straight'])
                elif score < 200:
                    enemy_type = random.choice(['sine', 'zigzag', 'shooter', 'straight'])
                else:  # score >= 200
                    enemy_type = random.choice(['sine', 'zigzag', 'shooter', 'straight'])

                # Calculate vx based on score for slightly more variation
                vx_scale = 1.5 + (min(score, 200) / 200) * 0.5
                new_enemy = {
                    'x': enemy_x,
                    'y': 0,
                    'base_x': enemy_x,
                    'type': enemy_type,
                    'vx': random.choice([-1, 1]) * vx_scale,
                    'amplitude': chosen_amplitude,
                    'spawn_frame': frame_count,
                    'shoot_cooldown': 0,
                    'warning_timer': 0
                }
                if enemy_type == 'shooter':
                    # Shooter cooldown: shorter as score increases
                    if score < 150:
                        base_cooldown = 80
                    elif score < 200:
                        base_cooldown = 60
                    else:
                        base_cooldown = 45
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
                    warning_duration = 10
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
                            # Use current_enemy_bullet_speed cooldown based on shooter config
                            if score < 150:
                                base_cooldown = 80
                            elif score < 200:
                                base_cooldown = 60
                            else:
                                base_cooldown = 45
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
                        # Use current_enemy_bullet_speed cooldown based on shooter config
                        if score < 150:
                            base_cooldown = 80
                        elif score < 200:
                            base_cooldown = 60
                        else:
                            base_cooldown = 45
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

            # Update reflectable projectiles
            for proj in reflectable_projectiles[:]:
                proj['x'] += proj['vx']
                proj['y'] += proj['vy']
                # Spin the projectile
                proj['rotation'] += 5
                # Remove if off screen
                if proj['x'] < -30 or proj['x'] > SCREEN_WIDTH + 30 or proj['y'] < -30 or proj['y'] > SCREEN_HEIGHT + 30:
                    reflectable_projectiles.remove(proj)
            
            # Update crash minions
            for m in swarm_minions[:]:
                m['x'] += m['vx']
                m['y'] += m['vy']
                if m['x'] < -40 or m['x'] > SCREEN_WIDTH + 40 or m['y'] > SCREEN_HEIGHT + 40:
                    swarm_minions.remove(m)
                    continue
                if not invincible:
                    if (player_x < m['x'] + 10 and player_x + player_width > m['x'] - 10 and
                        player_y < m['y'] + 25 and player_y + player_height > m['y'] - 5):
                        swarm_minions.remove(m)
                        player_hp -= 1
                        if player_hp <= 0:
                            game_state = 'game_over'
                        else:
                            invincible = True
                            invincible_timer = invincible_duration
                        continue

            # Update grabbers
            for g in grabbers[:]:
                if g.get('attached', False):
                    g['x'] = player_x + player_width // 2
                    g['y'] = player_y - 10
                else:
                    # Home in
                    dx = player_x + player_width // 2 - g['x']
                    dy = player_y + player_height // 2 - g['y']
                    dist = math.hypot(dx, dy) or 1
                    speed = g['vy']
                    g['x'] += (dx / dist) * speed
                    g['y'] += (dy / dist) * speed
                    if not invincible and (abs(g['x'] - (player_x + player_width // 2)) < 20 and abs(g['y'] - (player_y + player_height // 2)) < 20):
                        g['attached'] = True
                        grabbed = True
                        grab_escape_meter = 0
                # Remove if player escaped and grabber detached
                if not grabbed and g.get('attached', False):
                    grabbers.remove(g)
                    continue
                if g['y'] > SCREEN_HEIGHT + 50:
                    grabbers.remove(g)

            # Update multiplying bullets
            for b in multiplying_bullets[:]:
                b['x'] += b['vx']
                b['y'] += b['vy']
                bounced = False
                if b['x'] < 0 or b['x'] > SCREEN_WIDTH:
                    b['vx'] *= -1
                    bounced = True
                if b['y'] < 0 or b['y'] > SCREEN_HEIGHT:
                    b['vy'] *= -1
                    bounced = True
                if bounced:
                    b['bounces'] += 1
                b['split_timer'] -= 1
                if b['split_timer'] <= 0 and b['split_count'] < 2:
                    b['split_count'] += 1
                    b['split_timer'] = 50 - 5 * b['split_count']
                    # Create two off-angle bullets
                    for angle_delta in [-25, 25]:
                        angle = math.radians(angle_delta)
                        cos_a = math.cos(angle)
                        sin_a = math.sin(angle)
                        new_vx = b['vx'] * cos_a - b['vy'] * sin_a
                        new_vy = b['vx'] * sin_a + b['vy'] * cos_a
                        multiplying_bullets.append({'x': b['x'], 'y': b['y'], 'vx': new_vx, 'vy': new_vy, 'split_timer': b['split_timer'], 'bounces': b['bounces'], 'split_count': b['split_count']})
                if b['bounces'] > 4:
                    multiplying_bullets.remove(b)

            # Update exploding bullets
            for eb in exploding_bullets[:]:
                eb['x'] += eb['vx']
                eb['y'] += eb['vy']
                eb['fuse'] -= 1
                if eb['fuse'] <= 0:
                    # Explosion check
                    explosion_radius = 90
                    player_center = (player_x + player_width // 2, player_y + player_height // 2)
                    dist = math.hypot(player_center[0] - eb['x'], player_center[1] - eb['y'])
                    if dist < explosion_radius:
                        player_hp -= 1 if not invincible else 0
                        if player_hp <= 0:
                            game_state = 'game_over'
                        else:
                            invincible = True
                            invincible_timer = invincible_duration
                    exploding_bullets.remove(eb)
                    continue
                if eb['x'] < -40 or eb['x'] > SCREEN_WIDTH + 40 or eb['y'] < -40 or eb['y'] > SCREEN_HEIGHT + 40:
                    exploding_bullets.remove(eb)

            # Update lasers
            for lw in laser_warnings[:]:
                lw['charge'] -= 1
                if lw['charge'] <= 0:
                    active_lasers.append({'start': lw['start'], 'end': lw['end'], 'life': 60})
                    laser_warnings.remove(lw)
            for al in active_lasers[:]:
                al['life'] -= 1
                # Player hit check (line vs point simplified by distance to segment)
                if not invincible:
                    px = player_x + player_width // 2
                    py = player_y + player_height // 2
                    x1, y1 = al['start']
                    x2, y2 = al['end']
                    # projection
                    dx = x2 - x1
                    dy = y2 - y1
                    if dx == 0 and dy == 0:
                        dist = math.hypot(px - x1, py - y1)
                    else:
                        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx*dx + dy*dy)))
                        proj_x = x1 + t * dx
                        proj_y = y1 + t * dy
                        dist = math.hypot(px - proj_x, py - proj_y)
                    if dist < 12:
                        player_hp = 0
                        game_state = 'game_over'
                    if game_state == 'game_over':
                        active_lasers.clear()
                        laser_warnings.clear()
                        break
                if al['life'] <= 0:
                    active_lasers.remove(al)

            # Update path hazards
            for path in path_hazards[:]:
                path['duration'] -= 1
                # Check player inside corridor union
                px = player_x + player_width // 2
                py = player_y + player_height // 2
                inside = any(rect.collidepoint(px, py) for rect in path['rects'])
                if not inside:
                    player_hp = 0
                    game_state = 'game_over'
                    path_hazards.clear()
                    break
                if path['duration'] <= 0:
                    path_hazards.remove(path)

            # Update enemy bullets
            for eb in enemy_bullets[:]:
                eb[0] += eb[2]
                eb[1] += eb[3]
                if eb[0] < -10 or eb[0] > SCREEN_WIDTH + 10 or eb[1] < -10 or eb[1] > SCREEN_HEIGHT + 10:
                    enemy_bullets.remove(eb)

            # Update player bullets
            for bullet in bullets[:]:
                bullet[0] += bullet[2]
                bullet[1] += bullet[3]
                if bullet[0] < -bullet_width or bullet[0] > SCREEN_WIDTH or bullet[1] < -bullet_height or bullet[1] > SCREEN_HEIGHT:
                    bullets.remove(bullet)

            # Check bullet collisions with reflectable projectiles
            for bullet in bullets[:]:
                for proj in reflectable_projectiles[:]:
                    if not proj['reflected']:
                        # Check collision
                        dist = math.hypot(bullet[0] - proj['x'], bullet[1] - proj['y'])
                        if dist < 20:
                            bullets.remove(bullet)
                            # Reflect projectile back towards boss
                            if boss:
                                dx = boss['x'] + boss['width'] // 2 - proj['x']
                                dy = boss['y'] + boss['height'] // 2 - proj['y']
                                dist_to_boss = math.hypot(dx, dy)
                                if dist_to_boss > 0:
                                    proj['vx'] = (dx / dist_to_boss) * 5
                                    proj['vy'] = (dy / dist_to_boss) * 5
                                    proj['reflected'] = True
                            break

            # Check reflected projectiles hitting boss
            for proj in reflectable_projectiles[:]:
                if proj['reflected'] and boss:
                    # Check collision with boss
                    if (proj['x'] > boss['x'] - 15 and proj['x'] < boss['x'] + boss['width'] + 15 and
                        proj['y'] > boss['y'] - 15 and proj['y'] < boss['y'] + boss['height'] + 15):
                        reflectable_projectiles.remove(proj)
                        boss['hp'] -= 2  # Reflected projectiles do more damage
                        if boss['hp'] <= 0:
                            boss = None
                            reflectable_projectiles.clear()
                            swarm_minions.clear()
                            grabbers.clear()
                            multiplying_bullets.clear()
                            exploding_bullets.clear()
                            laser_warnings.clear()
                            active_lasers.clear()
                            path_hazards.clear()
                            score += 50
                        break

            # Check bullet-boss collisions (only when vulnerable, damage varies by boss type)
            if boss and boss.get('vulnerable', False):
                for bullet in bullets[:]:
                    if (bullet[0] < boss['x'] + boss['width'] and
                        bullet[0] + bullet_width > boss['x'] and
                        bullet[1] < boss['y'] + boss['height'] and
                        bullet[1] + bullet_height > boss['y']):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        if boss.get('type') == 'star':
                            dmg = 0.15
                        elif boss.get('type') == 'alien':
                            dmg = 0.35
                        else:
                            dmg = 1
                        boss['hp'] -= dmg
                        if boss['hp'] <= 0:
                            boss = None
                            swarm_minions.clear()
                            grabbers.clear()
                            multiplying_bullets.clear()
                            exploding_bullets.clear()
                            laser_warnings.clear()
                            active_lasers.clear()
                            path_hazards.clear()
                            score += 50
                        break

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

            # Check player hit by multiplying bullets
            if not invincible:
                for mb in multiplying_bullets[:]:
                    if (player_x < mb['x'] + 6 and
                        player_x + player_width > mb['x'] - 6 and
                        player_y < mb['y'] + 6 and
                        player_y + player_height > mb['y'] - 6):
                        multiplying_bullets.remove(mb)
                        player_hp -= 1
                        if player_hp <= 0:
                            game_state = 'game_over'
                        else:
                            invincible = True
                            invincible_timer = invincible_duration
                        break

            # Check player hit by unreflected projectiles
            if not invincible:
                for proj in reflectable_projectiles[:]:
                    if not proj['reflected']:
                        dist = math.hypot(player_x + player_width // 2 - proj['x'], player_y + player_height // 2 - proj['y'])
                        if dist < 25:
                            reflectable_projectiles.remove(proj)
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