"""
Módulo que define os inimigos do jogo.
"""

from game.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY
from game.EnemyShot import EnemyShot
from game.Entity import Entity

class Enemy(Entity):
    """Representa um inimigo que se move automaticamente e dispara periodicamente.

    Inimigos surgem pela borda direita da tela e avançam para a esquerda em linha
    reta. Atiram em intervalos fixos definidos por ENTITY_SHOT_DELAY. São destruídos
    ao perder toda a vida (por projéteis do jogador) ou ao sair pela borda esquerda.
    """
    def __init__(self, name: str, position: tuple):
        """
        Args:
            name: 'Enemy1', 'Enemy2' ou 'Enemy3', determina atributos e cadência de tiro.
            position: Posição inicial (x, y) — gerada aleatoriamente pelo EntityFactory.
        """
        super().__init__(name, position)
        # Contador regressivo de frames até o próximo disparo.
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):
        """Move o inimigo horizontalmente da direita para a esquerda.

        Ao sair pela borda esquerda, o EntityMediator define health=0,
        removendo o inimigo da lista de entidades sem conceder pontos ao jogador.
        """
        self.rect.centerx -= ENTITY_SPEED[self.name]

    def shoot(self):
        """Controla o disparo automático do inimigo.

        A cada frame decrementa o contador. Quando atinge zero, dispara um projétil
        a partir da sua posição atual e reinicia o cooldown.

        Returns:
            Um objeto EnemyShot na posição do inimigo, ou None se ainda em cooldown.
        """
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name] # reinicia o cooldown
            return EnemyShot(name=f"{self.name}Shot",
                             position=(self.rect.centerx, self.rect.centery))
        return None