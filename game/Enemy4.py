"""
Módulo que define o inimigo com movimento em zigue-zague.
"""

import math
from game.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY
from game.EnemyShot import EnemyShot
from game.Entity import Entity


class Enemy4(Entity):
    """Inimigo que se move em zigue-zague usando função seno.

    Avança horizontalmente da direita para a esquerda enquanto oscila
    verticalmente em ondas — tornando-o mais difícil de acertar que os
    inimigos com movimento reto.
    """

    def __init__(self, position: tuple):
        super().__init__("Enemy4", position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.frame = 0          # contador de frames — alimenta o math.sin()
        self.amplitude = 3      # altura da oscilação em pixels por frame
        self.frequency = 0.05   # frequência da onda — menor = oscilação mais suave

    def move(self):
        """Move o inimigo para a esquerda oscilando verticalmente em ondas."""
        self.rect.centerx -= ENTITY_SPEED[self.name]

        # math.sin() retorna valores entre -1 e +1
        # multiplicado pela amplitude define o deslocamento vertical a cada frame
        self.rect.centery += int(self.amplitude * math.sin(self.frame * self.frequency))
        self.frame += 1

    def shoot(self) -> EnemyShot | None:
        """Dispara um projétil com o mesmo comportamento dos outros inimigos."""
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(
                name="Enemy4Shot",
                position=(self.rect.centerx, self.rect.centery)
            )
        return None