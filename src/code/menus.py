import pygame
from pygame.locals import *


class Button(pygame.sprite.Sprite):
    def __init__(self, game, button_type):
        super().__init__()
        self.game = game
        button_path = "resources/images/"
        match button_type:
            case "start":
                button_path = button_path + "start_button.png"
                # location = center of screen, get from game
            case "unpause":
                button_path = button_path + "unpause_button.png"
                # location = one above center of screen
            case "restart":
                button_path = button_path + "restart_button.png"
                # if gamestate is pause, location is center
                # else location is half of one above center
            case "quit":
                button_path = button_path + "quit_button.png"
                # if gamestate is pause, location is one below center
                # else, gamestate is half of one below center
        self.image = pygame.image.load(button_path)
        self.rect = self.image.get_rect()
        # match for game state:
        # if start, only need start, center screen
        # if pause, need 3 buttons, need certain order
        # end needs two buttons, also certain order.
        # maybe not match - maybe we load "location" above, and use it below?
        # START GAME
        # UNPAUSE
        # RESTART
        # QUIT GAME
