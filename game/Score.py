"""
Módulo que define as telas de cadastro e exibição do ranking de pontuações.
"""

import datetime
import sys

import pygame
from pygame import Surface, Rect
from pygame.constants import K_ESCAPE
from pygame.font import Font

from game.Const import COLOR_YELLOW, SCORE_POS, MenuOption, COLOR_WHITE, resource_path
from game.DBProxy import DBProxy


class Score:
    """Gerencia as telas de pontuação: cadastro após vitória e exibição do ranking.

    Usa DBProxy para persistir e recuperar scores do banco de dados SQLite,
    mantendo as responsabilidades de UI e de acesso a dados separadas.
    """

    def __init__(self, window: Surface):
        """
        Args:
            window: Superfície principal onde as telas de score serão desenhadas.
        """
        self.window = window
        self.image = pygame.image.load(resource_path("./assets/ScoreBg.png")).convert_alpha()
        self.rect = self.image.get_rect()

    def save(self, game_mode: str, player_score: list[int]):
        """Exibe a tela de "YOU WIN!" e coleta o nome do vencedor para salvar no ranking.

        O jogador digita um nome de exatamente 4 caracteres e confirma com ENTER.
        A lógica de qual score salvar varia conforme o modo de jogo:
            • 1P: score do Player1.
            • 2P Cooperativo: média dos dois scores.
            • 2P Competitivo: score do jogador com maior pontuação.

        Args:
            game_mode: Modo de jogo (um dos valores de MENU_OPTION).
            player_score: Lista [score_p1, score_p2] ao final da partida.
        """
        pygame.mixer_music.load(resource_path("./assets/Score.mp3"))
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy("DBScore")

        name = "" # nome digitado pelo jogador (máximo 4 caracteres)

        while True:
            # Redesenha o fundo e o título a cada frame para manter a tela atualizada
            self.window.blit(source=self.image, dest=self.rect)
            self.score_text(48, "YOU WIN!", COLOR_YELLOW, SCORE_POS["Title"])

            # Define o score a salvar e o texto de instrução conforme o modo de jogo
            if game_mode == MenuOption.ONE_PLAYER:  # 1 jogador
                score = player_score[0]
                text = "Player 1 name: "

            elif game_mode == MenuOption.COOP:  # 2P cooperativo: média dos scores
                score = (player_score[0] + player_score[1]) / 2
                text = "Enter team name: "

            elif game_mode == MenuOption.COMPETITIVE:  # 2P competitivo: melhor score vence
                if player_score[0] >= player_score[1]:
                    score = player_score[0]
                    text = "Enter Player 1 name: "
                else:
                    score = player_score[1]
                    text = "Enter Player 2 name: "

            self.score_text(20, text, COLOR_WHITE, SCORE_POS["EnterName"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) == 4:
                        # Salva no banco e exibe o ranking atualizado
                        db_proxy.save({
                            "name": name,
                            "score": score,
                            "date": get_formatted_date()
                        })
                        self.show()
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1] # apaga o último caractere
                    else:
                        if len(name) < 4:
                            name += event.unicode # adiciona o caractere digitado

            # Exibe o nome sendo digitado em tempo real
            self.score_text(20, name, COLOR_WHITE, SCORE_POS["Name"])
            pygame.display.flip()

    def show(self):
        """Exibe o ranking dos 10 melhores scores armazenados no banco de dados.

        Permanece na tela até o jogador pressionar ESC para voltar ao menu.
        """
        pygame.mixer_music.load(resource_path("./assets/Score.mp3"))
        pygame.mixer_music.play(-1)

        # Desenha o fundo uma vez (a tela de ranking não precisa de animação)
        self.window.blit(self.image, self.rect)
        self.score_text(48, "TOP 10 SCORE", COLOR_WHITE, SCORE_POS["Title"])
        self.score_text(20, "NAME     SCORE              DATE      ", COLOR_WHITE, SCORE_POS["Label"])

        # Recupera e exibe os scores do banco
        db_proxy = DBProxy("DBScore")
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for i, record in enumerate(list_score):
            id_, name, score, date = record
            self.score_text(20,   f"{name}     {score:05d}      {date}", COLOR_YELLOW,
                            SCORE_POS[i])

        # Aguarda ESC para retornar
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip()

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        """Renderiza um texto centralizado em uma posição da tela de score.

        Args:
            text_size: Tamanho da fonte em pontos.
            text: Conteúdo do texto.
            text_color: Cor RGB do texto.
            text_center_pos: Coordenada (x, y) do centro do texto.
        """
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surface: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surface.get_rect(center=text_center_pos)
        self.window.blit(source=text_surface, dest=text_rect)

def get_formatted_date() -> str:
    """Retorna a data e hora atual formatadas para exibição no ranking.

    Returns:
        String no formato 'HH:MM - DD/MM/AAAA'.
    """
    return datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")