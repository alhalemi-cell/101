import battlesim.models as m
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

@dataclass(frozen=True)
class Config:
    class Pygame:
        SCREEN_WIDTH: int = 800
        SCREEN_HEIGHT: int = 600
        
    class Controls:
        INPUTS: list[tuple[str, str]] = [
                ("a", "(a)ttack"),
                ("s", "(s)witch"),
                ("q", "(q)uit"),
                ]
        BATTLE_INPUTS: list[tuple[str, str]] = [
                ("1", "move (1)"),
                ("2", "move (2)"),
                ("3", "move (3)"),
                ("4", "move (4)"),
                ]

@dataclass(frozen=True)
class Assets:
    SPRITE_DIR: str = "assets/sprites"
    SOUND_DIR: str = "assets/sounds"
    HIT_SOUND: str = "IMHIT.wav"
    FAINT_SOUND: str = "IMDOWN.wav"

@dataclass(frozen=True)
class Sprite:
    FRAME_TIME: int = 100

@dataclass(frozen=True)
class UI:
    class HealthBar:
        BAR_WIDTH: int = 200
        BAR_HEIGHT: int = 15

    class Font:
        FONT_NAME: str | None = "arial"
        FONT_SIZE: int = 24

    class Colors:
        WHITE: tuple[int, int, int] = (255, 255, 255)
        BLACK: tuple[int, int, int] = (0, 0, 0)
        GREEN: tuple[int, int, int] = (45, 200, 95)
        YELLOW: tuple[int, int, int] = (240, 200, 50)
        RED: tuple[int, int, int] = (220, 50, 50)
        GRAY: tuple[int, int, int] = (150, 150, 150)
        
        BG_SKY: tuple[int, int, int] = (135, 206, 235)    # Light Blue
        BG_GROUND: tuple[int, int, int] = (144, 238, 144) # Light Green
        PANEL_BG: tuple[int, int, int] = (248, 248, 248)  # Off-White
        PANEL_BORDER: tuple[int, int, int] = (70, 70, 70) # Dark Gray

@dataclass(frozen=True)
class Moves:
    # FIRE-TYPE MOVES
    FIRE_BREATH: m.Move = m.Move("Fire Breath", m.MonsterType.FIRE, 50)
    FLAME_BURST: m.Move = m.Move("Flame Burst", m.MonsterType.FIRE, 70)
    WING_SLASH: m.Move = m.Move("Wing Slash", m.MonsterType.FIRE, 55)
    DRAGON_FLARE: m.Move = m.Move("Dragon Flare", m.MonsterType.FIRE, 80)
    FIRE_FANG: m.Move = m.Move("Fire Fang", m.MonsterType.FIRE, 55)
    INFERNO_CHARGE: m.Move = m.Move("Inferno Charge", m.MonsterType.FIRE, 80)
    SPEED_TACKLE: m.Move = m.Move("Speed Tackle", m.MonsterType.FIRE, 60)
    BURNING_HOWL: m.Move = m.Move("Burning Howl", m.MonsterType.FIRE, 40)
    FIRE_KICK: m.Move = m.Move("Fire Kick", m.MonsterType.FIRE, 65)
    BLAZING_UPPERCUT: m.Move = m.Move("Blazing Uppercut", m.MonsterType.FIRE, 85)
    COMBAT_STRIKE: m.Move = m.Move("Combat Strike", m.MonsterType.FIRE, 60)
    HEAT_WAVE: m.Move = m.Move("Heat Wave", m.MonsterType.FIRE, 75)
    FIRE_BLAST: m.Move = m.Move("Fire Blast", m.MonsterType.FIRE, 90)
    ERUPTION_SURGE: m.Move = m.Move("Eruption Surge", m.MonsterType.FIRE, 95)
    EMBER_STORM: m.Move = m.Move("Ember Storm", m.MonsterType.FIRE, 60)
    FLARE_PULSE: m.Move = m.Move("Flare Pulse", m.MonsterType.FIRE, 70)

    # WATER-TYPE MOVES
    WATER_CANNON: m.Move = m.Move("Water Cannon", m.MonsterType.WATER, 80)
    MUD_HAMMER: m.Move = m.Move("Mud Hammer", m.MonsterType.WATER, 70)
    TIDAL_CRASH: m.Move = m.Move("Tidal Crash", m.MonsterType.WATER, 75)
    EARTH_SURGE: m.Move = m.Move("Earth Surge", m.MonsterType.WATER, 80)
    WATER_BEAM: m.Move = m.Move("Water Beam", m.MonsterType.WATER, 60)
    AQUA_PULSE: m.Move = m.Move("Aqua Pulse", m.MonsterType.WATER, 55)
    HYDRO_WAVE: m.Move = m.Move("Hydro Wave", m.MonsterType.WATER, 70)
    WATER_RAGE: m.Move = m.Move("Water Rage", m.MonsterType.WATER, 65)
    DRAGON_ROAR: m.Move = m.Move("Dragon Roar", m.MonsterType.WATER, 70)
    TIDAL_FURY: m.Move = m.Move("Tidal Fury", m.MonsterType.WATER, 85)
    AERIAL_CRUSH: m.Move = m.Move("Aerial Crush", m.MonsterType.WATER, 85)
    HYDRO_CANNON: m.Move = m.Move("Hydro Cannon", m.MonsterType.WATER, 95)
    SHELL_TACKLE: m.Move = m.Move("Shell Tackle", m.MonsterType.WATER, 70)
    PRESSURE_JET: m.Move = m.Move("Pressure Jet", m.MonsterType.WATER, 75)
    AQUA_BARRAGE: m.Move = m.Move("Aqua Barrage", m.MonsterType.WATER, 85)
    
    # WATER HEALING MOVE
    MIST_HEAL: m.Move = m.Move("Mist Heal", m.MonsterType.WATER, 0, m.MoveEffect.HEAL)

    # GRASS-TYPE MOVES
    VINE_WHIP: m.Move = m.Move("Vine Whip", m.MonsterType.GRASS, 40)
    SEED_BURST: m.Move = m.Move("Seed Burst", m.MonsterType.GRASS, 55)
    LEAF_SHOT: m.Move = m.Move("Leaf Shot", m.MonsterType.GRASS, 50)
    SOLAR_BEAM: m.Move = m.Move("Solar Beam", m.MonsterType.GRASS, 90)
    PETAL_STORM: m.Move = m.Move("Petal Storm", m.MonsterType.GRASS, 80)
    VINE_CRUSH: m.Move = m.Move("Vine Crush", m.MonsterType.GRASS, 70)
    LEAF_BLADE: m.Move = m.Move("Leaf Blade", m.MonsterType.GRASS, 75)
    FOREST_STRIKE: m.Move = m.Move("Forest Strike", m.MonsterType.GRASS, 65)
    QUICK_SLASH: m.Move = m.Move("Quick Slash", m.MonsterType.GRASS, 55)
    ENERGY_PULSE: m.Move = m.Move("Energy Pulse", m.MonsterType.GRASS, 60)
    WOOD_HAMMER: m.Move = m.Move("Wood Hammer", m.MonsterType.GRASS, 85)
    DRUM_BEAT: m.Move = m.Move("Drum Beat", m.MonsterType.GRASS, 70)
    ROOT_SMASH: m.Move = m.Move("Root Smash", m.MonsterType.GRASS, 80)
    NATURE_RUMBLE: m.Move = m.Move("Nature Rumble", m.MonsterType.GRASS, 75)
    
    # GRASS HEALING / STATUS MOVES
    NATURE_HEAL: m.Move = m.Move("Nature Heal", m.MonsterType.GRASS, 0, m.MoveEffect.HEAL)
    TOXIC_SPORES: m.Move = m.Move("Toxic Spores", m.MonsterType.GRASS, 30, m.MoveEffect.STATUS, "poison")

@dataclass(frozen=True)
class Monsters:
    CHARIZARD: m.Monster = m.Monster("Charizard", m.MonsterType.FIRE, 78, 84, 78, 100, m.Ability.SOLAR_POWER, m.MoveContainer(Moves.FIRE_BREATH, Moves.FLAME_BURST, Moves.WING_SLASH, Moves.DRAGON_FLARE))
    ARCANINE: m.Monster = m.Monster("Arcanine", m.MonsterType.FIRE, 90, 110, 80, 95, m.Ability.JUSTIFIED, m.MoveContainer(Moves.FIRE_FANG, Moves.INFERNO_CHARGE, Moves.SPEED_TACKLE, Moves.BURNING_HOWL))
    BLAZIKEN: m.Monster = m.Monster("Blaziken", m.MonsterType.FIRE, 80, 120, 70, 80, m.Ability.SPEED_BOOST, m.MoveContainer(Moves.FIRE_KICK, Moves.BLAZING_UPPERCUT, Moves.COMBAT_STRIKE, Moves.HEAT_WAVE))
    TYPHLOSION: m.Monster = m.Monster("Typhlosion", m.MonsterType.FIRE, 78, 84, 78, 100, m.Ability.FLASH_FIRE, m.MoveContainer(Moves.FIRE_BLAST, Moves.ERUPTION_SURGE, Moves.EMBER_STORM, Moves.FLARE_PULSE))
    
    SWAMPERT: m.Monster = m.Monster("Swampert", m.MonsterType.WATER, 100, 110, 90, 60, m.Ability.DAMP, m.MoveContainer(Moves.WATER_CANNON, Moves.MUD_HAMMER, Moves.TIDAL_CRASH, Moves.EARTH_SURGE))
    VAPOREON: m.Monster = m.Monster("Vaporeon", m.MonsterType.WATER, 130, 65, 60, 65, m.Ability.HYDRATION, m.MoveContainer(Moves.WATER_BEAM, Moves.AQUA_PULSE, Moves.MIST_HEAL, Moves.HYDRO_WAVE))
    GYRADOS: m.Monster = m.Monster("Gyarados", m.MonsterType.WATER, 95, 125, 79, 81, m.Ability.MOXIE, m.MoveContainer(Moves.WATER_RAGE, Moves.DRAGON_ROAR, Moves.TIDAL_FURY, Moves.AERIAL_CRUSH))
    BLASTOISE: m.Monster = m.Monster("Blastoise", m.MonsterType.WATER, 79, 83, 100, 78, m.Ability.RAIN_DISH, m.MoveContainer(Moves.HYDRO_CANNON, Moves.SHELL_TACKLE, Moves.PRESSURE_JET, Moves.AQUA_BARRAGE))
    
    BULBASAUR: m.Monster = m.Monster("Bulbasaur", m.MonsterType.GRASS, 45, 49, 49, 45, m.Ability.CHLOROPHYLL, m.MoveContainer(Moves.VINE_WHIP, Moves.SEED_BURST, Moves.LEAF_SHOT, Moves.NATURE_HEAL))
    VENUSAUR: m.Monster = m.Monster("Venusaur", m.MonsterType.GRASS, 80, 82, 83, 80, m.Ability.CHLOROPHYLL, m.MoveContainer(Moves.SOLAR_BEAM, Moves.TOXIC_SPORES, Moves.PETAL_STORM, Moves.VINE_CRUSH))
    SCEPTILE: m.Monster = m.Monster("Sceptile", m.MonsterType.GRASS, 70, 85, 65, 120, m.Ability.UNBURDEN, m.MoveContainer(Moves.LEAF_BLADE, Moves.FOREST_STRIKE, Moves.QUICK_SLASH, Moves.ENERGY_PULSE))
    RILLABOOM: m.Monster = m.Monster("Rillaboom", m.MonsterType.GRASS, 100, 125, 90, 85, m.Ability.GRASSY_SURGE, m.MoveContainer(Moves.WOOD_HAMMER, Moves.DRUM_BEAT, Moves.ROOT_SMASH, Moves.NATURE_RUMBLE))

    MONSTERS_LIST: tuple[m.Monster, ...] = (CHARIZARD, ARCANINE, BLAZIKEN, TYPHLOSION, SWAMPERT, VAPOREON, GYRADOS, BLASTOISE, BULBASAUR, VENUSAUR, SCEPTILE, RILLABOOM)

class TypeRelations:
    TYPE_MULTIPLIER: float = 2.0

    @staticmethod
    def _relations() -> "Mapping[m.MonsterType, set[m.MonsterType]]":
        rel: dict[m.MonsterType, set[m.MonsterType]] = {
            m.MonsterType.WATER: {m.MonsterType.FIRE},
            m.MonsterType.FIRE: {m.MonsterType.GRASS},
            m.MonsterType.GRASS: {m.MonsterType.WATER},
        }
        return MappingProxyType(rel)

    @staticmethod
    def GetEffectiveMultiplier(attack_type: m.MonsterType, defend_type: m.MonsterType) -> float:
        relations: "Mapping[m.MonsterType, set[m.MonsterType]]" = TypeRelations._relations()
        if defend_type in relations[attack_type]:
            return 2.0
        if attack_type in relations[defend_type]:
            return 0.5
        return 1.0
