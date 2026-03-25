# CSI2999 Battle Sim Project
## Overview
This project is a turn-based battle simulator written in Python, inspired by the combat mechanics found in games like Pokémon.

The game is designed for two players sharing the same device to battle against each other. Players assemble teams of characters and take turns using abilities or switching characters until one team is completely defeated.

The project was developed as a class assignment to practice Python programming fundamentals, turn-based game logic, and collaborative development.

## Game Features
- 12 playable characters
- 3 elemental types: Fire, Water, and Grass
- 4 characters per type
- 4 unique abilities per character
- Team-based combat with three characters per player
- Turn-based battle system
- Local two-player gameplay

## How the Game Works

### Team Selection
- Player 1 selects their first character.
- Player 2 selects their first character.
- The process repeats until both players have three characters.

### Starting the Battle
- Each player selects which character they want to send out first.

### Turn-Based Combat
On each turn, a player may:
- Use one of their character’s four abilities, or
- Switch characters (which consumes their turn)

After one player takes their turn, the game allows the other player to take their turn.

### Victory Conditions
- A player wins when all characters on the opposing team are defeated.
- A player may also quit the game, resulting in an immediate victory for the opponent.

### After the Match
Players may choose to:
- Play again, or
- End the game.

## Technologies Used
- Python
- PyGame

## Setup
```bash
git clone https://github.com/eroessleroakland/csi2999-battlesim.git
cd csi2999-battlesim
python -m venv venv
. ./venv/bin/active
pip install -r requirements.txt
pip install -e .
```
