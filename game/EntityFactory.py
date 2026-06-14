"""
Módulo que implementa a Factory de entidades do jogo.
"""

import random

from game.Background import Background
from game.Const import WIN_WIDTH, WIN_HEIGHT
from game.Enemy import Enemy
from game.Player import Player
from game.HealthItem import HealthItem


class EntityFactory:
    """Fábrica estática responsável por instanciar as entidades do jogo.

    Implementa o padrão de projeto Factory Method: centraliza a criação de
    entidades, de modo que o restante do código não precisa conhecer os detalhes
    de construção de cada tipo (posições iniciais, quantidades, etc.).

    Todos os métodos são estáticos, pois a fábrica não mantém estado próprio.
    """
    @staticmethod
    def get_entity(entity_name: str, position: tuple=(0,0)):
        """Cria e retorna a entidade correspondente ao nome informado.

        Para backgrounds, retorna uma lista de sprites (par por camada para o loop).
        Para jogadores e inimigos, retorna uma única instância.

        Args:
        entity_name: Nome da entidade a criar (ex: 'Level1Bg', 'Player1', 'Enemy2').
        position: Posição inicial usada para backgrounds. Ignorada para jogadores
        e inimigos, que têm posições fixas ou aleatórias definidas aqui.

        Returns:
        Uma instância de Entity ou uma lista de instâncias (para backgrounds),
        ou None se o nome não for reconhecido.
        """
        match entity_name:
            case "Level1Bg":
                # Cria 7 camadas de background (Level1Bg0 a Level1Bg6).
                # Cada camada gera dois sprites: um dentro da tela e outro à direita,
                # formando o par necessário para o scroll infinito.
                list_bg = []
                for i in range(5): # level1bg images number
                    list_bg.append(Background(f"Level1Bg{i}", position))
                    list_bg.append(Background(f"Level1Bg{i}", position=(WIN_WIDTH, 0)))
                return list_bg

            case "Level2Bg":
                # Cria 5 camadas de background para o Level 2.
                list_bg = []
                for i in range(5): # level2bg images number
                    list_bg.append(Background(f"Level2Bg{i}", position))
                    list_bg.append(Background(f"Level2Bg{i}", position=(WIN_WIDTH, 0)))
                return list_bg

            case "Player1":
                # Posicionado à esquerda da tela, levemente acima do centro.
                return Player("Player1", (10, WIN_HEIGHT / 2 - 30))

            case "Player2":
                # Posicionado à esquerda da tela, levemente abaixo do centro.
                return Player("Player2", (10, WIN_HEIGHT / 2 + 30))

            case "Enemy1":
                # Surge pela borda direita em altura aleatória (evitando as bordas).
                return Enemy("Enemy1", (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))

            case "Enemy2":
                return Enemy("Enemy2", (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))

            case "Enemy3":
                return Enemy("Enemy3",(WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))

            case "HealthItem":
                return HealthItem(position=(WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))

        return None # nome não reconhecido