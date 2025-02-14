import pygame
from button import Button

class PauseMenu():
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)

        # Menu Buttons
        self.restart_button = Button(game, "restart")
        self.restart_button.resize(0.75)
        self.restart_button.set_center(game.game_width() - 150, 150)
        self.resume_button = Button(game, "resume")
        self.resume_button.resize(0.75)
        self.resume_button.set_center(game.game_width() - 150, 225)
        self.quit_button = Button(game, "quit")
        self.quit_button.resize(0.75)
        self.quit_button.set_center(game.game_width() - 150, 300)

        self.pause_menu_background = pygame.Surface((game.game_width(), game.game_height()))
        self.pause_menu_background.set_alpha(135)
        self.pause_menu_background.fill("grey")

        # Upgrade Buttons
        self.reload_button = Button(game, "empty")
        self.reload_button.resize(0.75)
        self.reload_button.set_center(200, 150)
        self.reload_font = pygame.font.Font.render(self.font,
                                                   "Bullets: {}".format(game.get_player().get_bullet_price()),
                                                   True,
                                                   "black")
        self.reload_font_rect = self.reload_font.get_rect(center=self.reload_button.get_center())

    def draw(self, surface):
        surface.blit(self.pause_menu_background, (0, 0))
        self.restart_button.draw(surface)
        self.resume_button.draw(surface)
        self.quit_button.draw(surface)

        self.reload_button.draw(surface)
        surface.blit(self.reload_font, self.reload_font_rect)

    def get_button(self, button):
        match button:
            case "restart":
                return self.restart_button
            case "resume":
                return self.resume_button
            case "quit":
                return self.quit_button
            case "reload":
                return self.reload_button

