# Space N Aliens!

Quick! The aliens invaded your galaxy. Fight back and take back your home! It won't be easy :)

A 2D spaceship alien shooter made entirely in Python using Pygame.

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
- **Mash A/D**: Break free if a grabber latches onto you

### Game Features
- **HP System**: 3 HP with color feedback (green/yellow/red) and 2s invincibility frames after hits
- **Resizable Window**: Play in any window size
- **Enemy Types**: Straight, sine, zigzag, and shooter variants unlocked by score milestones
- **Boss Progression**: Spawns at scores 100, 200, and 300+
  - **Boss 1 (100)**: Rectangular, spread + aimed shots, periodic vulnerability windows
  - **Boss 2 (200)**: Star with a central void, launches spinning squares you can reflect back; very low bullet damage unless boss is vulnerable
  - **Final Boss (300)**: Multi-stage alien (4 phases) with ramping speed and attacks (minion swarms, grabbers, multiplying shots, explosives, player-aimed lasers, and winding corridors)
- **Hazards & Patterns**:
  - **Grabbers**: Latch and freeze movement; mash A/D to escape before their lifespan ends
  - **Multiplying Shots**: Split on bounces (limited bounces) and then despawn
  - **Exploding Shots**: Timed fuse, visible blast ring on detonation
  - **Lasers**: Telegraph then fire as thick beams aimed edge-to-edge through the player’s position
  - **Winding Corridors** (late stages): Stay inside the drawn paths or take damage
- **UI/States**: Title, pause, and game-over screens with navigation buttons

### Game Objective
- Survive as long as possible by shooting purple aliens
- Avoid letting aliens reach the bottom of the screen (instant game over)
- Avoid colliding with aliens (lose 1 HP per collision)
- Score points by shooting aliens
- Game ends when your HP reaches 0 or an alien reaches the bottom
