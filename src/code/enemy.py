import pygame
from random import randint
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("resources/images/soldier.png")
        self.rect = self.image.get_rect(center=(randint(0, self.game.game_width()), -40))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip(0, 1)
        if self.rect.colliderect(self.game.get_ground_rect()):
            self.game.set_game_end()
