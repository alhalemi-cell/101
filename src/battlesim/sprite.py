import battlesim.constants as constants
import pygame
from dataclasses import dataclass
from typing import override
from enum import Enum
import os 

# Sprites from https://pokemondb.net/

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames: list[pygame.Surface], x: int, y: int, frame_time: int = constants.Sprite.FRAME_TIME):
        super().__init__()
        self.frames: list[pygame.Surface] = frames
        self.x: int = x
        self.y: int = y
        self.frame_time: int = frame_time

        self.current_frame: int = 0
        self.current_frame_time: int = 0
        self.image: pygame.Surface = self.frames[self.current_frame]
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))

    @override
    def update(self, delta_time: int):
        self.current_frame_time += delta_time
        while self.current_frame_time >= self.frame_time:
            self.current_frame_time -= self.frame_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]


class SpriteOrientation(Enum):
    FRONT_FACING = 0
    REAR_FACING = 1

class SpriteRecord:
    def __init__(self, sprite_id: str, orientation: SpriteOrientation, shiny: bool = False):
        self.sprite_id: str = sprite_id.lower()
        self.orientation: SpriteOrientation = orientation
        self.shiny: bool = shiny 

# TODO: Load from https://pokemondb.net; check for timeout before starting,
#       Will then need to process data into some sort of gif processor to extract each frame,
#       Then push all frames into...


class StaticMonsterSprite(pygame.sprite.Sprite):
    def __init__(self, monster_name: str, orientation: SpriteOrientation, x: int, y: int):
        super().__init__()
        path = os.path.join(constants.Assets.SPRITE_DIR, f"{monster_name.lower()}_front.png")
        
        try:
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (200, 200))
            if orientation == SpriteOrientation.REAR_FACING:
                self.image = pygame.transform.flip(self.image, True, False)
        except (FileNotFoundError, pygame.error):
            self.image = pygame.Surface((150, 150))
            self.image.fill((200, 200, 200))
            
        self.rect = self.image.get_rect(center=(x, y))
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
