## 🔧 Installation
1. Install Python  
Download: https://www.python.org/downloads/

2. Install Pygame  
```bash
pip install pygame
```

3. Run the Game  
From inside the `src` folder:
```bash
python main.py
```

## 🎮 Controls
Left / A – Move left  
Right / D – Move right  
Up / W / Space – Jump  
Esc – Quit

## 🧱 Level Maps (levelmaps.py)
Levels are defined as lists of text rows:
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
X → Solid block  
P → Player start  
. → Empty space

## 🎨 Player Animations
Player animation frames must exist in `assets/player/`:
```text
idle.png
run1.png
run2.png
jump.png
fall.png
player_cheer1.png (optional)
```

States:  
idle  
run  
jump  
fall  

The game loads, scales, and flips these automatically.

## 🌿 Tile System
Tile artwork loaded from `assets/tiles/`:
```text
grass_single.png
grass_block_left.png
grass_block_middle.png
grass_block_right.png
dirt.png
```

Tile logic:  
If no tile above → draw grass  
Else → draw dirt  

Grass type depends on neighbors:  
No neighbors → grass_single  
Left only → grass_block_right  
Right only → grass_block_left  
Both → grass_block_middle  

## 🧠 Camera System
Camera centers on the player:
```python
camera_x = player.rect.centerx - WIDTH // 2
```

Clamped so the world doesn’t scroll too far.

All objects are drawn with:
```python
draw_x = tile.x - camera_x
```

## 🏆 Final Victory Screen
After the final level, the game shows:
- Sky background  
- Ground platform  
- player_cheer1.png (scaled up)  
- “YOU WIN!” text  
Waits for key press before closing.

## 🧩 Main Components (Summary)
✔ Player class  
Handles: Input, Physics, Collision, Animation, Drawing

✔ Level builder  
Creates tiles from 'X' and determines player start 'P'.

✔ Tile renderer  
Decides grass/dirt tiles using neighbor rules.

✔ Camera helper  
Centers the view and applies scrolling.

✔ Main loop  
Initializes pygame, Loads assets, Runs game, Switches levels, Shows final screen

## 🚀 Possible Extensions
Collectibles and coins  
Enemies with simple AI  
Music and sound effects  
Parallax backgrounds  
Checkpoints and lives  
HUD (score, health)  
Level editor

## 📜 License
MIT License (recommended). Add a LICENSE file in the repo.
