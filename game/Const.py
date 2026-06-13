"""
Constantes globais do jogo Mountain Shooter.

Centraliza todos os valores de configuração — velocidades, vida, dano,
pontuação, teclas, dimensões de tela e eventos — para facilitar o balanceamento
sem precisar editar múltiplos arquivos.
"""

import pygame
from enum import Enum

# ---------------------------------------------------------------------------
# C — Cores (R, G, B)
# ---------------------------------------------------------------------------
COLOR_ORANGE = (255, 128, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 128, 0)
COLOR_CYAN = (0, 128, 128)

# ---------------------------------------------------------------------------
# E — Atributos das entidades
# ---------------------------------------------------------------------------

# Pixels deslocados por frame para cada entidade.
# Backgrounds com índice maior se movem mais rápido → efeito parallax.
ENTITY_SPEED = {
    "Level1Bg0": 0,
    "Level1Bg1": 1,
    "Level1Bg2": 2,
    "Level1Bg3": 3,
    "Level1Bg4": 4,
    "Level1Bg5": 5,
    "Level1Bg6": 6,
    "Level2Bg0": 0,
    "Level2Bg1": 1,
    "Level2Bg2": 2,
    "Level2Bg3": 3,
    "Level2Bg4": 4,
    "Player1": 3,
    "Player1Shot": 1, # projétil lento, mas preciso
    "Player2": 3,
    "Player2Shot": 3, # projétil mais rápido que o do Player1
    "Enemy1": 1,
    "Enemy1Shot": 5, # projétil rápido do inimigo básico
    "Enemy2": 1,
    "Enemy2Shot": 2, # projétil mais lento do inimigo avançado
    "HealthItem": 2,
}

# Pontos de vida iniciais de cada entidade.
# Backgrounds têm vida muito alta para nunca serem destruídos.
ENTITY_HEALTH = {
    "Level1Bg0": 999,
    "Level1Bg1": 999,
    "Level1Bg2": 999,
    "Level1Bg3": 999,
    "Level1Bg4": 999,
    "Level1Bg5": 999,
    "Level1Bg6": 999,
    "Level2Bg0": 999,
    "Level2Bg1": 999,
    "Level2Bg2": 999,
    "Level2Bg3": 999,
    "Level2Bg4": 999,
    "Player1": 300,
    "Player1Shot": 1, # projétil é destruído no primeiro impacto
    "Player2": 300,
    "Player2Shot": 1,
    "Enemy1": 50,
    "Enemy1Shot": 1,
    "Enemy2": 60,
    "Enemy2Shot": 1,
    "HealthItem": 1,
}

# Frames entre cada disparo de uma entidade.
# Valores maiores = cadência de tiro menor.
ENTITY_SHOT_DELAY = {
    "Player1": 20,
    "Player2": 15, # Player2 atira um pouco mais rápido
    "Enemy1": 100,
    "Enemy2": 200, # Enemy2 é mais lento para atirar
}

# Dano causado pela entidade ao colidir com outra.
#
# Colisões verificadas pelo EntityMediator:
#   • Enemy   vs PlayerShot → Enemy.health   -= PlayerShot.damage
#                              PlayerShot.health -= Enemy.damage
#   • Player  vs EnemyShot  → Player.health  -= EnemyShot.damage
#                              EnemyShot.health -= Player.damage
#
# NOTA: Player vs Enemy (corpo a corpo) não é verificado atualmente,
#       portanto Enemy1.damage e Enemy2.damage não são aplicados em jogo.

ENTITY_DAMAGE = {
    "Level1Bg0": 0,
    "Level1Bg1": 0,
    "Level1Bg2": 0,
    "Level1Bg3": 0,
    "Level1Bg4": 0,
    "Level1Bg5": 0,
    "Level1Bg6": 0,
    "Level2Bg0": 0,
    "Level2Bg1": 0,
    "Level2Bg2": 0,
    "Level2Bg3": 0,
    "Level2Bg4": 0,
    "Player1": 1,
    "Player1Shot": 25,
    "Player2": 1,
    "Player2Shot": 20,
    "Enemy1": 100,
    "Enemy1Shot": 25,
    "Enemy2": 125,
    "Enemy2Shot": 20,
    "HealthItem": 0,
}

# Pontuação associada a cada entidade.
# Para inimigos: valor somado ao score do jogador que deu o tiro final.
# NOTA: os valores de projéteis e backgrounds existem por completude da tabela,
# mas não são usados diretamente na lógica de pontuação atual.
ENTITY_SCORE = {
    "Level1Bg0": 0,
    "Level1Bg1": 0,
    "Level1Bg2": 0,
    "Level1Bg3": 0,
    "Level1Bg4": 0,
    "Level1Bg5": 0,
    "Level1Bg6": 0,
    "Level2Bg0": 0,
    "Level2Bg1": 0,
    "Level2Bg2": 0,
    "Level2Bg3": 0,
    "Level2Bg4": 0,
    "Player1": 1,
    "Player1Shot": 25,
    "Player2": 1,
    "Player2Shot": 20,
    "Enemy1": 1,
    "Enemy1Shot": 20,
    "Enemy2": 1,
    "Enemy2Shot": 15,
    "HealthItem": 0,
}

# ---------------------------------------------------------------------------
# Ev — Eventos personalizados do Pygame
# ---------------------------------------------------------------------------
# pygame.USEREVENT é o primeiro ID disponível para eventos do usuário.
EVENT_ENEMY = pygame.USEREVENT + 1 # dispara o spawn de um novo inimigo
EVENT_TIMEOUT = pygame.USEREVENT + 2 # decrementa o temporizador do nível
EVENT_HEALTH_ITEM = pygame.USEREVENT + 3

# ---------------------------------------------------------------------------
# M — Menu
# ---------------------------------------------------------------------------
# Classe com as opções exibidas no menu principal, na ordem em que aparecem.
class MenuOption(Enum):
    ONE_PLAYER  = "NEW GAME 1P"
    COOP        = "NEW GAME 2P - COOPERATIVE"
    COMPETITIVE = "NEW GAME 2P - COMPETITIVE"
    SCORE       = "SCORE"
    EXIT        = "EXIT"

# ---------------------------------------------------------------------------
# P — Teclas do jogador
# ---------------------------------------------------------------------------
PLAYER_KEY_UP    = {"Player1": pygame.K_UP,    "Player2": pygame.K_w}
PLAYER_KEY_DOWN  = {"Player1": pygame.K_DOWN,  "Player2": pygame.K_s}
PLAYER_KEY_LEFT  = {"Player1": pygame.K_LEFT,  "Player2": pygame.K_a}
PLAYER_KEY_RIGHT = {"Player1": pygame.K_RIGHT, "Player2": pygame.K_d}
PLAYER_KEY_SHOOT = {"Player1": pygame.K_RCTRL, "Player2": pygame.K_LCTRL}

# ---------------------------------------------------------------------------
# S — Spawn
# ---------------------------------------------------------------------------
SPAWN_TIME = 4000 # intervalo em milissegundos entre spawns de inimigos
SPAWN_HEALTH_ITEM = 45000 # aparece a cada 45 segundos

# ---------------------------------------------------------------------------
# T — Temporizador do nível
# ---------------------------------------------------------------------------
TIMEOUT_STEP = 100 # ms descontados a cada tick do EVENT_TIMEOUT
TIMEOUT_LEVEL = 20000 # duração total do nível em milissegundos (20 segundos)

# ---------------------------------------------------------------------------
# W — Janela
# ---------------------------------------------------------------------------
WIN_WIDTH = 576
WIN_HEIGHT = 324

# Posições centrais (x, y) dos textos na tela de pontuação.
SCORE_POS = {
    "Title":     (WIN_WIDTH / 2, 50),
    "EnterName": (WIN_WIDTH / 2, 80),
    "Label":     (WIN_WIDTH / 2, 90),
    "Name":      (WIN_WIDTH / 2, 110),
    0:           (WIN_WIDTH / 2, 110),
    1:           (WIN_WIDTH / 2, 130),
    2:           (WIN_WIDTH / 2, 150),
    3:           (WIN_WIDTH / 2, 170),
    4:           (WIN_WIDTH / 2, 190),
    5:           (WIN_WIDTH / 2, 210),
    6:           (WIN_WIDTH / 2, 230),
    7:           (WIN_WIDTH / 2, 250),
    8:           (WIN_WIDTH / 2, 270),
    9:           (WIN_WIDTH / 2, 290),
}