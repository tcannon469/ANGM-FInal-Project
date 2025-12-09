# Mini Python Platformer  
A simple 2D platformer built in Python, using Pygame plugin

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Pygame](https://img.shields.io/badge/pygame-2.5-orange)

---

## Overview

This project is a miniature 2D platformer game made inside Python, using the Pygame plugin.  
Features include:

- Animated player (idle, run, jump, fall)
- Grass/dirt auto-tiling terrain, easily rearrangable in the code
- Multi-level support (this project caps it at 3 for easy presenting)
- Proper in-game collision with walls
- Side-scrolling camera from level to level
- End screen upon completion
- Easily expandable code that's clean and concise

This project was done entirely from the perspective of a beginner and for beginners, to encourage an easier time to accomodate real-time game design. Assets were sampled from free-to-use databases to allow further time on coding and reiteration.

---

## Indepth Feature List

- Smooth player movement and jump physics for satisfying platformer movement/control 
- Animation system for the in-game sprites
- Automatic tile selection in the code (grass, dirt, edges, inbetween)  
- Level maps defined in simple text format for easier level editing/design  
- Camera following the player throughout, sidescrolling camera
- Easily expandable for further content, such as enemies, checkpoints, items, etc.

---

## Folder Structure

```text
project-root/
│
├── assets/
│   ├── player/
│   │   ├── idle.png
│   │   ├── run1.png
│   │   ├── run2.png
│   │   ├── jump.png
│   │   ├── fall.png
│   │   └── end_screen.png
│   │
│   └── tiles/
│       ├── grass_single.png
│       ├── grass_block_left.png
│       ├── grass_block_middle.png
│       ├── grass_block_right.png
│       └── dirt.png
│
├── src/
│   ├── main.py
│   ├── levelmaps.py
│   └── (your other modules)
│
└── README.md

```
## Installation
 
### 1. Install Python

Have Python 3.10+ installed!

Link to download: https://www.python.org/downloads/

### 2. Install Pygame

Type in a terminal or command prompt:
```
pip install pygame
```

### 3. Run the Game
From inside the `src` folder:
```bash
python main.py
```

## Controls
- Left / A = Move left  
- Right / D = Move right  
- Up / W / Space = Jump  
- Esc = Quit

## Level Maps (levelmaps.py)
Levels are defined as lists of text rows for easy customization:
```python
LEVEL_MAPS = [
    [
        "............................",
        "............................",
        "...P.............XXX........",
        ".............XXXXXXXX.......",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ]
]
```

Legend:

- X = Solid block
- P = Player starting point
- . = Empty space

## Player Animations
All player graphics were obtained from Kenney Platformer Art Characters

Link to source: https://kenney.nl/assets

Licensed under CC0/Public Domain laws

All player animation frames must exist in `assets/player/`.

```text
idle.png
run1.png
run2.png
jump.png
fall.png
player_cheer1.png (optional)
```

States:
The four animation states that exist in the game are:
 - idle
 - run
 - jump
 - fall

The game loads, scales, and flips these automatically.

## Tile System
Tile graphics obtained from Kenney Platformer Art Extended TileSet

Link to source: https://kenney.nl/assets

Licensed under CC0/Public Domain laws

All tile artwork must be loaded in `assets/tiles/`.

```text
grass_single.png
grass_block_left.png
grass_block_middle.png
grass_block_right.png
dirt.png
```

Tile Logic:
32×32 blocks compromise all tile sizes (TILE_SIZE = 32).

FOR each 'X' in the level:
- IF no tile above = draw grass blocks
- ELSE = draw dirt blocks instead

Types of grass depend on the neighbors: 
```
| Left neighbor | Right neighbor | Tile used          |
| ------------- | -------------- | ------------------ |
| none          | none           | grass_single       |
| none          | yes            | grass_block_left   |
| yes           | yes            | grass_block_middle |
| yes           | none           | grass_block_right  |
```

This process generates relatively natural-looking tiles to correspond with a semi-believable environment, without manual operation by the user.

## Camera System
Camera will always center on the player as they scroll through the level:
```python
camera_x = player.rect.centerx - WIDTH // 2
```

Camera will always manage to keep player in frame for playability

All objects relating to the camera are drawn with:
```python
draw_x = tile.x - camera_x
```
The x-position (movement) of tiles and player is shifted by camera_x

This achieves the side-scrolling effect, of the level moving to accomodate the player

## Victory/Completion Screen
Once completing the allotted levels, the game will:

- Show a sky background 
- Show the ground platform
- Show "player_cheer1.png", scaled up for clarity
- Show celebratory text saying "YOU WIN"

The program will then wait for a key to be pressed before closing

## Summary
Player Class

- This handles the player input, player physics, player collision, player animation, and player drawing

Tile/Level Builder

- This creates level tiles from 'X' and determines the start of the player at 'P'

Tile Renderer

- This decides whether to use grass or dirt tiles depending on established neighbor rules

Camera Control

- This determines the view of the camera to be centered, as well as applying scrolling

Main Loop

- This initializes the pygame module, loads all assets, runs the game itself, switches out levels upon completion and changing, and shows the celebratory winning screen upon completion

## Optional extensions I could make to my current work

I could add:

- Collectibles with distinct art

- Enemies that provide obstacles for the player, with simple AI

- Any music or sound effects to accompany the gameplay

- Parallax-scrolling backgrounds to provide depth to the environments

- A checkpoint and life system to add both more aid and more stakes for the player to contend with

- A HUD/ingame UI to display health, level progress, etc.

- An accessible in-game level editor, since the tech to easily edit levels exists in the code

## License
MIT License
