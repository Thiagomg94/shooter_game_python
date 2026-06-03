from game.Const import WIN_WIDTH, ENTITY_SPEED
from game.Entity import Entity

class Background(Entity):
    """Representa uma camada de fundo que se move em loop horizontal.

    O cenário é composto por múltiplas instâncias de Background com velocidades
    diferentes (definidas em ENTITY_SPEED), produzindo um efeito de parallax:
    camadas mais distantes se movem mais devagar, criando sensação de profundidade.

    Cada camada possui um par de imagens posicionadas lado a lado — uma começa
    dentro da tela e a outra imediatamente à direita. Quando a primeira sai pela
    esquerda, ela é reposicionada à direita da segunda, formando um scroll infinito.
    """
    def __init__(self, name: str, position: tuple):
        """
        Args:
            name: Identificador da camada (ex: 'Level1Bg2'). O número ao final
            determina a velocidade — índice maior = camada mais próxima = mais rápida.
            position: Posição inicial (x, y) do canto superior esquerdo da imagem.
        """
        super().__init__(name, position)

    def move(self):
        """Desloca o background para a esquerda e faz o reposicionamento em loop.
            Quando o lado direito do sprite ultrapassa o limite esquerdo da tela,
            o sprite é movido para o início da tela à direita, criando scroll contínuo.
        """
        self.rect.centerx -= ENTITY_SPEED[self.name] # movimenta para a esquerda

        # Ao sair completamente da tela pela esquerda, reposiciona à direita
        # para continuar o loop de scrolling sem interrupções visíveis.
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH