# Space N Aliens!

Quick! The aliens invaded your galaxy. Fight back and drive them out! It won't be easy :)

## Guide

### Prerequisites
- Python 3.x
- Pygame library

### Installation
1. Clone the repository: `git clone https://github.com/tbaaaa/space-n-aliens.git`
2. Navigate to the project directory: `cd space-n-aliens`
3. Install dependencies: `pip install pygame`

### Running the Game
Run the game with: `python main.py`

The game window is resizable - you can maximize, restore, or resize it as needed.

### Controls
- **A/D Keys**: Move the spaceship left/right
- **W/S Keys**: Move the spaceship up/down
- **Left Mouse Button**: Aim and shoot bullets (aim with mouse cursor)
- **ESC Key**: Pause the game
- **E Key**: Toggle debug invincibility (ship turns cyan when active)
- **Mash A/D**: Break free if a grabber latches onto you

### Game Features

#### Visual & Atmosphere
- **Resizable Window**: Play in any window size
- **Dynamic Space Background**: Scrolling star field with progressive speeds (1.5x to 5.5x based on score)
- **Distant Planets**: Randomly spawning planets with environment-based colors
- **Environment Progression**: Background colors evolve through 4 levels (dark blue → purple → reddish)
- **Hyperdrive Cutscene**: 6-second cinematic travel sequence after defeating each boss
  - Screen flash effects
  - Ship shake animation
  - 15x accelerated star/planet speed
  - 3-second post-immunity with flashing ship

#### Combat System
- **HP System**: 3 HP with color feedback (green/yellow/red) and 2s invincibility frames after hits
- **Enemy Types**: Straight, sine, zigzag, and shooter variants unlocked by score milestones
- **Warning System**: Shooter enemies and turrets flash before firing (6-frame warning)

#### Enemy Turrets (Unlocked by Boss Defeats)
- **Side Turrets (Orange)**: Unlock after defeating Boss 1
  - Spawn on left/right edges at score 100+
  - Move up/down, shoot at player
  - 1 HP, worth 5 points
- **Horizontal Turrets (Cyan)**: Unlock after defeating Boss 2
  - Spawn on top/bottom edges at score 200+
  - Move left/right, shoot at player
  - 1 HP, worth 5 points

#### Boss Progression
Bosses spawn at scores 100, 200, and 300+

- **Boss 1 (100)**: Rectangular boss
  - Spread + aimed shots
  - Periodic vulnerability windows
  - Unlocks side turrets upon defeat

- **Boss 2 (200)**: Star-shaped boss
  - Launches spinning reflectable squares (purple → yellow when reflected)
  - 8-way bursts, spirals, and triple spreads
  - Very low bullet damage unless reflected projectiles are used
  - Unlocks horizontal turrets upon defeat

- **Final Boss (300+)**: Multi-stage alien
  - 4 progressive stages based on remaining HP
  - Always vulnerable but extremely tanky
  - Unique attacks per stage:
    - **Swarm Minions**: Red triangular enemies that home in on player
    - **Grabbers**: Cyan tentacle enemies that latch and freeze movement (mash A/D to escape)
    - **Multiplying Bullets**: Magenta shots that split on wall bounces
    - **Exploding Bullets**: Orange delayed explosions with visible fuse timers
    - **Telegraph Lasers**: Player-aimed laser beams with yellow warning phase
    - **Winding Corridors** (Stage 4): Streaming bullet walls that follow the boss's path

#### Hazards & Patterns
- **Reflectable Projectiles**: Shoot purple squares to reflect them back at bosses (deal 2x damage)
- **Grabbers**: Latch and freeze movement; mash A/D to escape before their lifespan ends
- **Multiplying Shots**: Split on bounces (limited bounces) then despawn
- **Exploding Shots**: Timed fuse with visible blast ring on detonation
- **Lasers**: Telegraph then fire as thick beams aimed edge-to-edge
- **Winding Corridors**: Boss moves to top, corridor bullets converge from screen edges

#### UI/States
- Title screen with Start/Exit buttons
- Pause functionality (ESC key)
- Game-over screen with Restart/Exit options
- Real-time HP display with color-coded health bar

### Game Objective
- Survive as long as possible by shooting purple aliens
- Defeat all three bosses to progress through environments
- Avoid letting aliens reach the bottom of the screen
- Avoid colliding with aliens and enemy projectiles
- Score points by destroying enemies and turrets
- Game ends when your HP reaches 0

### Debug Features
- Press **E** to toggle invincibility mode
- Invincible ship displays in cyan color
- Useful for testing boss patterns and late-game content
