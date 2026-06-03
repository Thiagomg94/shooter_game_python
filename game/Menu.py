"""
Módulo que define o menu principal do jogo.
"""

import pygame
from pygame import Surface, Rect
from pygame.font import Font
from game.Const import WIN_WIDTH, COLOR_ORANGE, COLOR_WHITE, MenuOption, COLOR_YELLOW


class Menu:
    """Tela de menu principal com navegação por teclado.

        Exibe as opções de jogo e aguarda a seleção do usuário pelas teclas
        direcional para cima/baixo e ENTER. A opção selecionada é destacada
        em amarelo; as demais permanecem em branco.
        """

    def __init__(self, window):
        """
        Args:
            window: Superfície principal do Pygame onde o menu será desenhado.
        """
        self.window = window
        self.image = pygame.image.load("./assets/MenuBg.png").convert_alpha()
        self.rect = self.image.get_rect()
        pygame.mixer_music.load("./assets/Menu.mp3")

    def run(self) :
        """Exibe o menu e aguarda a seleção do usuário.

        Processa eventos de teclado para navegação entre opções e confirmação.
        A música do menu toca em loop enquanto o menu está ativo.

        Returns:
            A string da opção selecionada (um dos valores de MENU_OPTION).
        """
        menu_option = 0 # índice da opção atualmente destacada
        pygame.mixer_music.play(-1) # -1 = repetir indefinidamente
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    options = list(MenuOption)
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(options)
                    if event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(options)
                    if event.key == pygame.K_RETURN:
                        return options[menu_option]  # retorna o membro do Enum, não a string

            self.window.fill("black")
            self.window.blit(self.image, self.rect)

            # Título do jogo
            self.menu_text(text_size=50,
                           text="Mountain",
                           text_color=COLOR_ORANGE,
                           text_center_pos=((WIN_WIDTH / 2), 70))

            self.menu_text(text_size=50,
                           text="Shooter",
                           text_color=COLOR_ORANGE,
                           text_center_pos=((WIN_WIDTH / 2), 120))

            # Renderiza cada opção; a selecionada usa cor diferente para destaque
            options = list(MenuOption)  # converte os membros do Enum em lista para iterar
            for i, mode in enumerate(options):
                color = COLOR_YELLOW if i == menu_option else COLOR_WHITE
                self.menu_text(20, mode.value, color, (WIN_WIDTH / 2, 200 + 20 * i))

            pygame.display.flip()
            clock.tick(60)

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        """Renderiza um texto centralizado em uma posição da tela.

        Args:
            text_size: Tamanho da fonte em pontos.
            text: Conteúdo do texto a exibir.
            text_color: Cor RGB do texto.
            text_center_pos: Coordenada (x, y) do centro do texto.
        """
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surface: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surface.get_rect(center=text_center_pos)
        self.window.blit(source=text_surface, dest=text_rect)