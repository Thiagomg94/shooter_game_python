"""
Módulo que define a lógica de um nível do jogo.
"""

import random
import sys

import pygame
from pygame import Surface, Rect
from pygame.font import Font

from game.Const import COLOR_BLACK, WIN_HEIGHT, MenuOption, EVENT_ENEMY, SPAWN_TIME, COLOR_GREEN, COLOR_CYAN, \
    EVENT_TIMEOUT, TIMEOUT_STEP, TIMEOUT_LEVEL, EVENT_HEALTH_ITEM, SPAWN_HEALTH_ITEM
from game.Enemy import Enemy
from game.Entity import Entity
from game.EntityFactory import EntityFactory
from game.EntityMediator import EntityMediator
from game.Player import Player


class Level:
    """Gerencia um nível completo do jogo: entidades, eventos, HUD e condições de término.

        Responsável por:
            • Instanciar o background e os jogadores via EntityFactory.
            • Executar o loop principal (game loop) do nível.
            • Controlar o spawn periódico de inimigos via eventos do Pygame.
            • Detectar fim de nível (timeout ou morte de todos os jogadores).
            • Atualizar o score compartilhado entre níveis.
        """

    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        """Inicializa o nível, criando background, jogadores e configurando os timers.

               Args:
                   window: Superfície principal onde o nível será desenhado.
                   name: Nome do nível ('Level1' ou 'Level2'), usado para carregar assets.
                   game_mode: Modo de jogo selecionado no menu (determina número de jogadores).
                   player_score: Lista [score_p1, score_p2] herdada do nível anterior.
                                 Permite que a pontuação persista entre os níveis.
               """

        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.timeout = TIMEOUT_LEVEL
        self.entity_list: list[Entity] = []

        # Carrega as camadas de background (parallax)
        self.entity_list.extend(EntityFactory.get_entity(self.name + "Bg"))

        # Cria Player1 e restaura a pontuação acumulada do nível anterior
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)

        # Adiciona Player2 apenas nos modos de dois jogadores
        if game_mode in [MenuOption.COOP, MenuOption.COMPETITIVE]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)

        # Configura os timers periódicos de spawn de inimigos e timeout do nível.
        # Chamar set_timer novamente com o mesmo evento substitui o timer anterior,
        # então não há vazamento de timers entre níveis.
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)
        pygame.time.set_timer(EVENT_HEALTH_ITEM, SPAWN_TIME)

    def run(self, player_score: list[int]):
        """Executa o loop principal do nível até que ele termine.

                O nível termina de duas formas:
                    • Timeout atingido → retorna True (jogadores sobreviveram, avançam ao próximo nível).
                    • Todos os jogadores morrem → retorna False (game over).

                Args:
                    player_score: Lista mutável [score_p1, score_p2] atualizada ao final do nível.

                Returns:
                    True se o nível foi completado com sucesso; False se todos os jogadores morreram.
                """
        pygame.mixer_music.load(f"./assets/{self.name}.mp3")
        pygame.mixer_music.play(-1) # toca a música do nível em loop
        clock = pygame.time.Clock()

        while True:
            clock.tick(60) # limita o loop a 60 frames por segundo

            # --- Atualização e renderização das entidades ---
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect) # desenha o sprite
                ent.move() # move a entidade conforme a sua lógica

                # Jogadores e inimigos podem disparar; projéteis são adicionados à lista
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

                # Exibe HUD com vida e pontuação de cada jogador
                if ent.name == "Player1":
                    self.text_level(text_size=14, text=f"Player 1 - Health: {ent.health} | Score: {ent.score}",
                                    text_color=COLOR_GREEN, text_pos=(10, 25))
                if ent.name == "Player2":
                    self.text_level(text_size=14, text=f"Player 2 - Health: {ent.health} | Score: {ent.score}",
                                    text_color=COLOR_CYAN, text_pos=(10, 45))

            # --- Processamento de eventos ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == EVENT_ENEMY:
                    # Spawna um inimigo aleatório pela borda direita
                    choice_enemy = random.choice(("Enemy1", "Enemy2", "Enemy3"))
                    self.entity_list.append(EntityFactory.get_entity(choice_enemy))

                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout == 0:
                        # Nível concluído: salva a pontuação final de cada jogador
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == "Player1":
                                player_score[0] = ent.score
                            if isinstance(ent, Player) and ent.name == "Player2":
                                player_score[1] = ent.score
                        return True # jogadores sobreviveram

                if event.type == EVENT_HEALTH_ITEM:
                    self.entity_list.append(EntityFactory.get_entity("HealthItem"))

            # --- Verificação de jogadores vivos ---
            if not any(isinstance(ent, Player) for ent in self.entity_list):
                return False  # todos os jogadores morreram → game over

            # --- HUD: informações de debug e tempo restante ---
            self.text_level(text_size=14, text=f"{self.name} - Timeout: {self.timeout / 1000:.1f}s",
                            text_color=COLOR_BLACK, text_pos=(10, 5))

            self.text_level(text_size=14, text=f"fps: {clock.get_fps():.0f}",
                            text_color=COLOR_BLACK, text_pos=(10, WIN_HEIGHT - 35))

            self.text_level(text_size=14, text=f"entidades: {len(self.entity_list)}",
                            text_color=COLOR_BLACK, text_pos=(10, WIN_HEIGHT - 20))

            pygame.display.flip()

            # Detecta e resolve colisões, depois remove entidades sem vida
            EntityMediator.verify_collision(self.entity_list)
            EntityMediator.verify_health(self.entity_list)

    def text_level(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        """Renderiza um texto alinhado à esquerda em uma posição da tela.

                Args:
                    text_size: Tamanho da fonte em pontos.
                    text: Conteúdo do texto a exibir.
                    text_color: Cor RGB do texto.
                    text_pos: Coordenada (x, y) do canto superior esquerdo do texto.
                """
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)