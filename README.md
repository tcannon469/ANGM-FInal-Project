# 🕹️ Mini Python Platformer
*A simple 2D platformer built with Python + Pygame*

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Pygame](https://img.shields.io/badge/pygame-2.5-orange)

---

## 📌 Overview
This project is a fully animated side-scrolling platformer built using **Python** and **Pygame**.  
It includes:
- Animated player (idle, run, jump, fall)
- Automatic grass/dirt tile selection
- Smooth side-scrolling camera
- Simple physics and collisions
- Multi-level system via text maps
- "You Win" final screen
- Clean, extendable codebase

---

## 📂 Folder Structure

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
│   │   └── player_cheer1.png
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
