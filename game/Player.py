"""
Módulo que define o jogador controlado pelo usuário.
"""

import pygame

from game.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from game.Entity import Entity
from game.PlayerShot import PlayerShot


class Player(Entity):
    """Representa um jogador controlado por teclado.

    Suporta dois perfis independentes ('Player1' e 'Player2'), cada um com
    seu próprio mapeamento de teclas definido em Const.py, permitindo o modo
    cooperativo/competitivo com dois jogadores no mesmo teclado.
    """
    def __init__(self, name: str, position: tuple):
        """
        Args:
            name: 'Player1' ou 'Player2', determina teclas e atributos.
            position: Posição inicial (x, y) do sprite.
        """
        super().__init__(name, position)
        # Contador regressivo de frames até o próximo disparo permitido.
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):
        """Move o jogador com base nas teclas pressionadas no frame atual.

        O movimento é limitado pelas bordas da tela para evitar que o sprite
        saia da área visível.
        """
        pressed_key = pygame.key.get_pressed()

        # Movimento vertical — verifica limites superior e inferior da tela
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += ENTITY_SPEED[self.name]

        # Movimento horizontal — verifica limites esquerdo e direito da tela
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]

    def shoot(self):
        """Controla o disparo do jogador com base no delay de recarga.

        Decrementa o contador a cada frame. Quando chega a zero, verifica se a
        tecla de disparo está pressionada e, em caso positivo, cria e retorna um
        novo projétil posicionado no centro do jogador.

        Returns:
                Um objeto PlayerShot se o disparo ocorreu, ou None caso contrário.
        """
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name] # reinicia o cooldown
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                return PlayerShot(name=f"{self.name}Shot", position=(self.rect.centerx, self.rect.centery))
        return None