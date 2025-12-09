# Mini Platformer Game – Full Documentation

## 1. Project Overview
This document explains the structure and behavior of the mini platformer game written in Python using the Pygame library. The game includes side-scrolling levels, grass and dirt tiles, an animated character, level transitions, and an optional victory screen.

## 2. Dependencies and Imports
### `pygame`
Handles rendering, window creation, keyboard input, timing, and collision rectangles.

### `sys`
Used for `sys.exit()` to quit cleanly.

### `os`
Used for building cross-platform file paths.

### `from levelmaps import LEVEL_MAPS`
Imports level definitions from a separate Python file.

## 3. Global Settings and Paths
- Screen: 800×600 pixels  
- TILE_SIZE: 32 × 32  
- FPS: 60  
- Colors: SKY_BLUE, RED  
- Asset paths: `assets/player/` and `assets/tiles/`

## 4. Player Class
Handles physics, animation, movement, collisions, and drawing.

### Physics:
- `vel_x`, `vel_y`
- `speed`, `jump_power`
- `gravity`, `max_fall_speed`
- `on_ground`

### Animation:
- `state` (`idle`, `run`, `jump`, `fall`)
- `facing_right`
- `frame_index`, `anim_speed`

## 4.1 Animation Loading
Loads PNG sprites:
- idle.png
- run1.png, run2.png
- jump.png
- fall.png

Uses `.convert_alpha()` and rescaling.

## 4.2 Input, Physics, and Collision
- Arrow keys / WASD for movement
- SPACE / W / UP to jump
- Split-axis collision system prevents clipping into tiles

## 4.3 Animation + Drawing
Updates animation state, flips sprite if needed, offsets by camera position, and draws onto the screen.

## 5. Level Building and Camera
`build_level()`:
- Creates tiles for `'X'`
- Stores player start for `'P'`

`get_camera_x()`:
- Centers camera on player
- Clamped to level boundaries

## 6. Tile Images and Terrain Logic
Loaded images:
- grass_single
- grass_left
- grass_middle
- grass_right
- dirt

Logic checks neighbors:
- If no block above → use grass variants
- If block above → use dirt

## 7. Final End Screen
Displays:
- Sky background  
- Ground  
- Cheering sprite (`player_cheer1.png`)  
- “YOU WIN!” text  

Waits for keypress before exiting.

## 8. Main Game Loop
Handles:
- Initialization
- Event processing
- Player update
- Level transitions
- Camera scrolling
- Tile + player rendering
- Display flipping
- Cleanup

## 9. Image Usage Summary
### Player sprites:
- idle.png  
- run1.png  
- run2.png  
- jump.png  
- fall.png  
- player_cheer1.png (optional)

### Tile sprites:
- grass_single.png  
- grass_block_left.png  
- grass_block_middle.png  
- grass_block_right.png  
- dirt.png  

## 10. Future Extensions
- Enemies  
- Collectibles  
- Background parallax  
- More animations  
- Sound and music  
- HUD / Score  
- Level editor  

