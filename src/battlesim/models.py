from __future__ import annotations
from enum import Enum
from typing import override, Callable
import random

class MonsterType(Enum):
    GRASS = 0
    FIRE = 1
    WATER = 2

class Ability(Enum):
    NONE = 0
    SOLAR_POWER = 1  
    JUSTIFIED = 2    
    SPEED_BOOST = 3  
    FLASH_FIRE = 4   
    DAMP = 5         
    HYDRATION = 6    
    MOXIE = 7        
    RAIN_DISH = 8    
    CHLOROPHYLL = 9  
    UNBURDEN = 10    
    GRASSY_SURGE = 11

class MoveEffect(Enum):
    DAMAGE = 0
    HEAL = 1
    STATUS = 2

class Monster:
    def __init__(self, name: str, monster_type: MonsterType, max_health: int, damage: int, defense: int, speed: int, ability: Ability, moves: MoveContainer):
        self.name: str = name
        self.monster_type: MonsterType = monster_type
        self.max_health: int = max_health
        self.current_health: int = max_health
        self.damage: int = damage
        self.defense: int = defense
        self.speed: int = speed
        self.ability: Ability = ability
        self.moves: MoveContainer = moves

        self.fainted: bool = False
        self.is_asleep: bool = False
        self.current_sleep_turns: int = 0
        self.is_leech_seeded: bool = False
        self.is_poisoned: bool = False 

    def can_attack(self) -> bool:
        if self.is_asleep:
            self.current_sleep_turns -= 1
            if self.current_sleep_turns <= 0:
                self.is_asleep = False
                print(f"{self.name} woke up!")
                return True
            return False
        return True

    def apply_ability_effects_on_attack(self, fainted_enemy: Monster):
        if self.ability == Ability.MOXIE and fainted_enemy.fainted:
            self.damage += 15
            print(f"{self.name}'s Moxie increased its attack!")

    def calculate_damage(self, move: Move, defending_monster: Monster, multiplier: Callable[[MonsterType, MonsterType], float]) -> tuple[int, float, bool]:
        if move not in self.moves.moves or move.effect_type != MoveEffect.DAMAGE:
            return 0, 1.0, False

        if defending_monster.ability == Ability.FLASH_FIRE and move.type == MonsterType.FIRE:
            return 0, 0.0, False

        effective_attack = float(self.damage)
        if self.ability == Ability.SOLAR_POWER:
            effective_attack *= 1.5

        if defending_monster.speed > self.speed * 1.25 and random.random() < 0.15:
            return 0, 0.0, False

        effectiveness = multiplier(move.type, defending_monster.monster_type)
        stab = 1.5 if move.type == self.monster_type else 1.0
        is_crit = random.random() < 0.0625 
        crit_multiplier = 1.5 if is_crit else 1.0

        base_damage = (float(move.power) * effective_attack / float(defending_monster.defense))
        damage: int = int(base_damage * effectiveness * stab * crit_multiplier) 
        
        return max(1, damage) if effectiveness > 0 else 0, effectiveness, is_crit

    def attack(self, move: Move, defending_monster: Monster, multiplier: Callable[[MonsterType, MonsterType], float]) -> str:
        if not self.can_attack():
            return f"{self.name} is fast asleep!"

        message = f"{self.name} used {move.name}! "
        
        if move.effect_type == MoveEffect.HEAL:
            heal_amount = self.max_health // 2
            self.heal(heal_amount)
            return message + f"Recovered HP!"
            
        elif move.effect_type == MoveEffect.STATUS:
            if move.status_effect == "poison" and not defending_monster.is_poisoned:
                defending_monster.is_poisoned = True
                message += f"{defending_monster.name} was poisoned! "
            elif move.status_effect == "leech" and not defending_monster.is_leech_seeded:
                defending_monster.is_leech_seeded = True
                message += f"{defending_monster.name} was seeded! "
            damage, eff, crit = self.calculate_damage(move, defending_monster, multiplier) if move.power > 0 else (0, 1.0, False)
            
        else:
            damage, eff, crit = self.calculate_damage(move, defending_monster, multiplier)
            
        if eff > 1.0:
            message += "It's super effective! "
        elif eff < 1.0 and eff > 0.0:
            message += "It's not very effective... "
        elif eff == 0.0:
            message += "It had no effect! "
            
        if crit and damage > 0:
            message += "A critical hit! "

        if damage > 0:
            defending_monster.current_health -= damage
            if defending_monster.current_health <= 0:
                defending_monster.fainted = True
                message += f"{defending_monster.name} fainted!"
                self.apply_ability_effects_on_attack(defending_monster)
                
        return message

    def end_of_turn(self):
        if self.is_poisoned and not self.fainted:
            poison_dmg = max(1, self.max_health // 8)
            self.take_damage(poison_dmg)
            print(f"{self.name} took {poison_dmg} damage from poison!")
        if not self.fainted:
            if self.ability == Ability.SPEED_BOOST:
                self.speed += 10
                print(f"{self.name}'s Speed Boost increased its speed!")
            elif self.ability == Ability.CHLOROPHYLL:
                self.speed += 5 
            elif self.ability == Ability.RAIN_DISH:
                self.heal(max(1, self.max_health // 16))
            elif self.ability == Ability.GRASSY_SURGE:
                if self.monster_type == MonsterType.GRASS:
                    self.heal(max(1, self.max_health // 16))
            elif self.ability == Ability.SOLAR_POWER:
                self.take_damage(max(1, self.max_health // 10))
            elif self.ability == Ability.HYDRATION and self.is_poisoned:
                self.is_poisoned = False
                print(f"{self.name}'s Hydration cured its poison!")

    def take_damage(self, amount: int):
        self.current_health -= int(amount)
        if self.current_health <= 0:
            self.current_health = 0
            self.fainted = True

    def heal(self, amount: int):
        self.current_health += amount
        self.current_health = self.current_health if self.current_health <= self.max_health else self.max_health

    @override
    def __str__(self) -> str:
        return f"Name: {self.name}, Type: {self.monster_type}, Health: {self.current_health}, Atk: {self.attack}, Def: {self.defense}, Spd: {self.speed}, Ability: {self.ability.name}, Moves: {self.moves}"

class Move:
    def __init__(self, name: str, type: MonsterType, power: int, effect_type: MoveEffect = MoveEffect.DAMAGE, status_effect: str = None):
        self.name: str = name
        self.type: MonsterType = type
        self.power: int = power
        self.effect_type: MoveEffect = effect_type
        self.status_effect: str = status_effect

    @override
    def __str__(self):
        return f"Name: {self.name}, Type: {self.type}, Power: {self.power}"

class MoveContainer:
    def __init__(self, move1: Move, move2: Move, move3: Move, move4: Move):
        self.moves: list[Move] = [move1, move2, move3, move4]
    
    def GetMove(self, i: int):
        return self.moves[i]

    def end_of_turn(self, opponent: "Monster" = None):
        if self.is_poisoned and not self.fainted:
            poison_dmg = max(1, self.max_health // 8)
            self.take_damage(poison_dmg)
            print(f"{self.name} took {poison_dmg} damage from poison!")
        if self.is_leech_seeded and not self.fainted and opponent:
            leech_dmg = max(1, self.max_health // 8)
            self.take_damage(leech_dmg)
            opponent.heal(leech_dmg)
            print(f"{self.name} had HP drained by Leech Seed!")

    

    @override
    def __str__(self):
        return f"Move1: {self.GetMove(0)}, Move2: {self.GetMove(1)}, Move3: {self.GetMove(2)}, Move4: {self.GetMove(3)}"
