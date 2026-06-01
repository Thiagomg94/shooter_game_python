import random

from game.Background import Background
from game.Const import WIN_WIDTH, WIN_HEIGHT
from game.Enemy import Enemy
from game.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position: tuple=(0,0)):
        match entity_name:
            case "Level1Bg":
                list_bg = []
                for i in range(7): # level1bg images number
                    list_bg.append(Background(f"Level1Bg{i}", position))
                    list_bg.append(Background(f"Level1Bg{i}", position=(WIN_WIDTH, 0)))
                return list_bg

            case "Level2Bg":
                list_bg = []
                for i in range(5): # level2bg images number
                    list_bg.append(Background(f"Level2Bg{i}", position))
                    list_bg.append(Background(f"Level2Bg{i}", position=(WIN_WIDTH, 0)))
                return list_bg

            case "Player1":
                return Player("Player1", (10, WIN_HEIGHT / 2 - 30))

            case "Player2":
                return Player("Player2", (10, WIN_HEIGHT / 2 + 30))

            case "Enemy1":
                return Enemy("Enemy1", (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))

            case "Enemy2":
                return Enemy("Enemy2", (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))
        return None
