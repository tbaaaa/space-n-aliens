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

### Game Features
- **HP System**: Your ship starts with 3 HP
- **Visual HP Indicator**: Ship color changes based on health:
  - 3 HP: Green
  - 2 HP: Yellow
  - 1 HP: Red
- **Invincibility Frames**: After taking damage, your ship flashes and becomes invincible for 2 seconds
- **Purple Aliens**: Shoot down the purple alien invaders before they reach you!
- **Collision System**: Aliens that touch your ship deal 1 damage and are destroyed
- **Pause Menu**: Press ESC to pause and access Resume, Back to Title, or Exit options
- **Multiple Screens**: Title screen, pause menu, and game over screen with various options

### Game Objective
- Survive as long as possible by shooting purple aliens
- Avoid letting aliens reach the bottom of the screen (instant game over)
- Avoid colliding with aliens (lose 1 HP per collision)
- Score points by shooting aliens
- Game ends when your HP reaches 0 or an alien reaches the bottom
