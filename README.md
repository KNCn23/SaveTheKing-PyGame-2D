# Save the King! — PyGame 2D

A top-down 2D RPG built with Python and Pygame. Escort the King through a dangerous world filled with bandits, locked doors, riddles, and secrets.

---

## Gameplay

You play as either a **Knight** (melee) or an **Archer** (ranged). Your goal is to guide the King safely to the castle while surviving ambushes, solving guard riddles, and looting chests along the way.

### Controls

| Key | Action |
|-----|--------|
| `W A S D` / Arrow keys | Move |
| `Space` / Left click | Attack |
| `E` | Interact (pick up item, open chest, talk to NPC) |
| `I` | Open / close inventory |
| `1` `2` `3` | Use item from inventory |
| `Tab` | Toggle full map |
| `Esc` | Pause menu |

Controller (Xbox/PS) is also supported.

---

## Classes

**Knight**
- 100 Vitality, 20 Attack Power
- Melee sword swing
- Higher effective armor

**Archer**
- 70 Vitality, 25 Attack Power
- Fires projectiles with left click (aim with mouse)
- Better at keeping distance

---

## Features

- 30+ hand-crafted interconnected rooms across forest, town, and dungeon regions
- Range-based enemy AI — melee bandits close in, archer bandits hold their distance and attack from range
- Friendly NPC dialogue with randomized reactions based on game state
- Guard riddle system — answer correctly to open the gate, fail three times and they turn hostile
- Merchant trading with gold coins
- Chest and item system with keys, health items, and armor
- Fog-of-war minimap that reveals as you explore
- King companion AI that follows and must be kept alive
- Save / load system

---

## Installation

**Requirements:** Python 3.10+ and Pygame

```bash
pip install pygame
python main.py
```

---

## Project Structure

```
main.py          — game loop, state machine, input handling
player.py        — Player, Knight, Archer classes + Projectile
enemy.py         — Enemy AI (melee / ranged)
characters.py    — King, Guard, NPC classes
level.py         — world map, room loading, transitions, minimap data
ui.py            — HUD, inventory, minimap, big map, dialogue box
item.py          — Item and Chest classes
save_system.py   — JSON save / load
config.py        — screen size, colors, constants
button_mapping.py — keyboard + controller input abstraction
assets/          — sprites, tilesets, sounds
```

---

## Screenshots

> *(coming soon)*

---

## License

MIT License — feel free to use, modify, and distribute.
