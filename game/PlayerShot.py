"""
Módulo que define o projétil disparado pelo jogador.
"""

from game.Const import ENTITY_SPEED
from game.Entity import Entity


class PlayerShot(Entity):
    """Projétil criado quando o jogador dispara.

    Move-se horizontalmente da esquerda para a direita (na direção dos inimigos).
    É destruído ao colidir com um inimigo ou ao sair pela borda direita da tela,
    conforme verificado pelo EntityMediator.
    """

    def __init__(self, name: str, position: tuple):
        """
        Args:
            name: Identificador do projétil ('Player1Shot' ou 'Player2Shot').
            position: Posição inicial (x, y) — normalmente o centro do jogador que atirou.
        """
        super().__init__(name, position)

    def move(self):
        """Move o projétil para a direita em direção aos inimigos."""
        self.rect.centerx += ENTITY_SPEED[self.name]