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
            case "resume":
                button_path = button_path + "resume_button.png"
            case "restart":
                button_path = button_path + "restart_button.png"
            case "quit":
                button_path = button_path + "quit_button.png"
            case "empty":
                button_path = button_path + "base_button.png"
        self.image = pygame.image.load(button_path)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def set_center(self, x, y):
        self.rect = self.image.get_rect(center=(x, y))

    def check_click(self, mouse):
        return self.rect.collidepoint(mouse)

    def resize(self, size):
        self.image = pygame.transform.scale_by(self.image, size)

    def get_center(self):
        return self.rect.center

