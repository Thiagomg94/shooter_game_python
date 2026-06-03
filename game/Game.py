"""
Módulo principal do jogo — ponto de entrada e controle do fluxo de telas.
"""

import pygame

from game.Const import WIN_WIDTH, WIN_HEIGHT, MenuOption
from game.Level import Level
from game.Menu import Menu
from game.Score import Score


class Game:
    """Controlador principal que gerencia o fluxo entre menu, níveis e ranking.

    Inicializa o Pygame e coordena a sequência de telas:
        Menu → Level1 → Level2 → Score (em caso de vitória)

    O loop principal em `run()` retorna sempre ao menu após cada partida,
    permitindo jogar múltiplas vezes sem reiniciar o programa.
    """

    def __init__(self):
        """Inicializa o Pygame e cria a janela principal do jogo."""
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        """Executa o loop principal de fluxo do jogo.

        Aguarda a seleção do menu e encaminha para a ação correspondente:
            • Modos de jogo (1P, 2P Coop, 2P Comp): executa Level1 e, se concluído,
                Level2. Ao completar ambos os níveis, redireciona para o cadastro de score.
            • SCORE: exibe o ranking diretamente.
            • EXIT: encerra o jogo de forma limpa.
        """
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in [MenuOption.ONE_PLAYER, MenuOption.COOP, MenuOption.COMPETITIVE]:
                
                player_score = [0, 0] # [Player1, Player2]

                # Executa o Nível 1; avança ao Nível 2 apenas se o jogador sobreviver
                level = Level(self.window, 'Level1', menu_return, player_score)
                level_return = level.run(player_score)

                if level_return:
                    # Executa o Nível 2; ao concluir, abre o cadastro de score
                    level = Level(self.window, 'Level2', menu_return, player_score)
                    level_return = level.run(player_score)

                    if level_return:
                        score.save(menu_return, player_score) # jogador vence os dois níveis

            elif menu_return == MenuOption.SCORE: # "SCORE"
                score.show()

            elif menu_return == MenuOption.EXIT: # "EXIT"
                pygame.quit()
                quit()