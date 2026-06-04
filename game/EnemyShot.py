"""
Módulo que define o projétil disparado pelos inimigos.
"""

from game.Const import ENTITY_SPEED
from game.Entity import Entity


class EnemyShot(Entity):
    """Projétil criado quando um inimigo dispara.

    Move-se horizontalmente da direita para a esquerda (na direção dos jogadores).
    É destruído ao colidir com um jogador ou ao sair pela borda esquerda da tela,
    conforme verificado pelo EntityMediator.
    """
    def __init__(self, name: str, position: tuple):
        """
        Args:
        name: Identificador do projétil ('Enemy1Shot' ou 'Enemy2Shot').
        position: Posição inicial (x, y) — normalmente o centro do inimigo que atirou.
        """
        super().__init__(name, position)

    def move(self):
        """Move o projétil para a esquerda em direção aos jogadores."""
        self.rect.centerx -= ENTITY_SPEED[self.name]