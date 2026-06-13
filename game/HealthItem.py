from game.Const import  ENTITY_SPEED
from game.Entity import Entity

HEALTH_RESTORE = 5 # quantidade de vida restaurada ao coletar

class HealthItem(Entity):
    def __init__(self, position):
        super().__init__("HealthItem", position)
        self.health = HEALTH_RESTORE

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]