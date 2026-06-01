from abc import ABC, abstractmethod
import pygame.image

from game.Const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE


class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.surf = pygame.image.load("./assets/" + name + '.png').convert_alpha()
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0
        if name not in ENTITY_HEALTH:
            raise ValueError(f" Entity {name} doesn't have health attribute.")
        self.health = ENTITY_HEALTH[name]
        if name not in ENTITY_DAMAGE:
            raise ValueError(f" Entity {name} doesn't have damage attribute.")
        self.damage = ENTITY_DAMAGE[name]
        self.score = ENTITY_SCORE[name]
        self.last_dmg = 'None'

    @abstractmethod
    def move(self):
        pass