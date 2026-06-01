import datetime
import sys

import pygame
from pygame import Surface, Rect
from pygame.constants import K_ESCAPE
from pygame.font import Font

from game.Const import COLOR_YELLOW, SCORE_POS, MENU_OPTION, COLOR_WHITE
from game.DBProxy import DBProxy


class Score:
    def __init__(self, window: Surface):
        self.window = window
        self.image = pygame.image.load("./assets/ScoreBg.png").convert_alpha()
        self.rect = self.image.get_rect()

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer_music.load("./assets/Score.mp3")
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy("DBScore")

        name = ""
        while True:
            self.window.blit(source=self.image, dest=self.rect)
            self.score_text(48, "YOU WIN!", COLOR_YELLOW, SCORE_POS["Title"])

            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
                text = "Player 1 name: "

            if game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) / 2
                text = "Enter team name: "

            if game_mode == MENU_OPTION[2]:
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
                        db_proxy.save({"name": name, "score": score, "date": get_formatted_date()})
                        self.show()
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 4:
                            name += event.unicode

            self.score_text(20, name, COLOR_WHITE, SCORE_POS["Name"])
            pygame.display.flip()

    def show(self):
        pygame.mixer_music.load("./assets/Score.mp3")
        pygame.mixer_music.play(-1)
        self.window.blit(self.image, self.rect)
        self.score_text(48, "TOP 10 SCORE", COLOR_WHITE, SCORE_POS["Title"])
        self.score_text(20, "NAME     SCORE              DATE      ", COLOR_WHITE, SCORE_POS["Label"])
        db_proxy = DBProxy("DBScore")
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for player in list_score:
            id_, name, score, date = player
            self.score_text(20,   f"{name}     {score:05d}      {date}", COLOR_YELLOW,
                            SCORE_POS[list_score.index(player)])

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
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surface: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surface.get_rect(center=text_center_pos)
        self.window.blit(source=text_surface, dest=text_rect)

def get_formatted_date():
    return datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")