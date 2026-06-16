"""
Módulo que define a classe base abstrata para todas as entidades do jogo.
"""

from abc import ABC, abstractmethod
import pygame.image

from game.Const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE, resource_path


class Entity(ABC):
    """Classe base abstrata para todas as entidades do jogo (jogadores, inimigos, projéteis, cenário).

    Define os atributos comuns (imagem, posição, vida, dano, pontuação) e exige
    que subclasses implementem o método `move()`, garantindo o contrato de movimento
    polimórfico usado no loop principal do jogo.
    """
    def __init__(self, name: str, position: tuple):
        """Inicializa a entidade carregando sua imagem e configurando seus atributos.

            Args:
                name: Identificador único da entidade (deve estar em ENTITY_HEALTH, ENTITY_DAMAGE
                e ENTITY_SCORE). Também define o nome do arquivo de imagem em ./assets/.
                position: Tupla (x, y) com a posição inicial do canto superior esquerdo do sprite.

            Raises:
                ValueError: Se `name` não existir nos dicionários de saúde ou dano.
        """
        self.name = name

        # Carrega o sprite correspondente ao nome da entidade.
        # convert_alpha() otimiza a superfície para renderização com transparência.
        #self.surf = pygame.image.load("./assets/" + name + '.png').convert_alpha()
        self.surf = pygame.image.load(resource_path("assets/" + name + '.png')).convert_alpha()

        # `get_rect` obtém o retângulo de colisão/posicionamento a partir da imagem.
        # `left` e `top` posicionam o canto superior esquerdo do sprite.
        self.rect = self.surf.get_rect(left=position[0], top=position[1])

        self.speed = 0 # velocidade base; velocidade real vem de ENTITY_SPEED em cada subclasse

        if name not in ENTITY_HEALTH:
            raise ValueError(f" Entity {name} doesn't have health attribute.")
        self.health = ENTITY_HEALTH[name]

        if name not in ENTITY_DAMAGE:
            raise ValueError(f" Entity {name} doesn't have damage attribute.")
        self.damage = ENTITY_DAMAGE[name]

        self.score = ENTITY_SCORE[name]

        # Registra o nome da última entidade que causou dano a esta.
        # Usado pelo EntityMediator para atribuir pontos ao jogador correto.
        self.last_dmg = "None"

    @abstractmethod
    def move(self):
        """Move a entidade de acordo com sua lógica específica de deslocamento.

        Deve ser implementado por cada subclasse (Background, Player, Enemy, etc.).
        Chamado a cada frame pelo loop principal do nível.
        """
        pass