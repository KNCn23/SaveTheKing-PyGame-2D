# Save the King — PyGame 2D

A top-down 2D RPG built with Python and Pygame. Escort the King through a dangerous world filled with bandits, locked doors, riddles, and secrets.

---

## Gameplay

Play as either a **Knight** (melee) or an **Archer** (ranged) and guide the King safely to the castle. Survive ambushes, answer guard riddles, and loot chests along the way.

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

Xbox and PlayStation controllers are also supported.

---

## Classes

**Knight**
- 100 HP, 20 Attack — melee sword swing, higher effective armor

**Archer**
- 70 HP, 25 Attack — projectile attacks aimed with mouse, better at range

---

## Features

- 30+ hand-crafted interconnected rooms across forest, town, and dungeon regions
- Range-based enemy AI — melee bandits close in, archer bandits hold distance
- Friendly NPC dialogue with state-aware randomized reactions
- Guard riddle system — fail three times and the guard turns hostile
- Merchant trading with gold coins
- Chest and item system with keys, health items, and armor
- Fog-of-war minimap that reveals as you explore
- King companion AI that follows and must survive
- Save / load system

---

## Installation

Requires Python 3.10+ and Pygame.

```bash
pip install pygame
python main.py
```

---

## Project Structure

```
main.py           — game loop, state machine, input handling
player.py         — Player, Knight, Archer classes and Projectile
enemy.py          — Enemy AI (melee / ranged)
characters.py     — King, Guard, NPC classes
level.py          — world map, room loading, transitions, minimap data
ui.py             — HUD, inventory, minimap, big map, dialogue box
item.py           — Item and Chest classes
save_system.py    — JSON save / load
config.py         — screen size, colors, constants
button_mapping.py — keyboard and controller input abstraction
assets/           — sprites, tilesets, sounds
```

---

## License

MIT
