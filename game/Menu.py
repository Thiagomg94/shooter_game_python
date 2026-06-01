import pygame
from pygame import Surface, Rect
from pygame.font import Font
from game.Const import WIN_WIDTH, COLOR_ORANGE, COLOR_WHITE, MENU_OPTION, COLOR_YELLOW


class Menu:
    def __init__(self, window):
        self.window = window
        self.image = pygame.image.load("./assets/MenuBg.png").convert_alpha()
        self.rect = self.image.get_rect()
        pygame.mixer_music.load("./assets/Menu.mp3")

    def run(self):

        menu_option = 0

        pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

            self.window.fill("black")

            self.window.blit(self.image, self.rect)

            self.menu_text(text_size=50,
                           text="Mountain",
                           text_color=COLOR_ORANGE,
                           text_center_pos=((WIN_WIDTH / 2), 70))

            self.menu_text(text_size=50,
                           text="Shooter",
                           text_color=COLOR_ORANGE,
                           text_center_pos=((WIN_WIDTH / 2), 120))

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(text_size=20,
                                   text=MENU_OPTION[i],
                                   text_color=COLOR_YELLOW,
                                   text_center_pos=((WIN_WIDTH / 2), 200 + 20 * i))

                else:
                    self.menu_text(text_size=20,
                                   text=MENU_OPTION[i],
                                   text_color=COLOR_WHITE,
                                   text_center_pos=((WIN_WIDTH / 2), 200 + 20 * i))

            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surface: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surface.get_rect(center=text_center_pos)
        self.window.blit(source=text_surface, dest=text_rect)