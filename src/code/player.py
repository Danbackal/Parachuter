from bullet import Bullet
import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    # Owns the player tank, as well as the bullets shot from the tank
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.tank_body = pygame.image.load("resources/images/tank_body.png")
        self.body_rect = self.tank_body.get_rect(center=(self.game.game_width()/2, 820))
        self.draw_body = self.tank_body
        self.draw_body_rectangle = self.body_rect
        self.tank_arm = pygame.image.load("resources/images/tank_arm.png")
        self.arm_rect = self.tank_arm.get_rect(center=(self.game.game_width()/2, 810))
        self.draw_arm = self.tank_arm
        self.draw_arm_rectangle = self.arm_rect
        self.arm_angle = 0
        self.bullet_group = pygame.sprite.Group()
        self.bullet_timer = 0

    def draw(self, surface):
        surface.blit(self.draw_body, self.draw_body_rectangle)
        surface.blit(self.draw_arm, self.draw_arm_rectangle)
        self.bullet_group.draw(surface)

    def update(self, pressed):
        # want to use match - case here but need to learn more about pressed first
        if pressed[K_RIGHT] and self.arm_angle > -90:
            self.arm_angle -= 1
            self.draw_arm = pygame.transform.rotate(self.tank_arm, self.arm_angle)
        if pressed[K_LEFT] and self.arm_angle < 90:
            self.arm_angle += 1
            self.draw_arm = pygame.transform.rotate(self.tank_arm, self.arm_angle)
        self.draw_arm_rectangle = self.draw_arm.get_rect(center=self.arm_rect.center)
        if pressed[K_SPACE] and self.bullet_timer <= 0:
            self.bullet_group.add(Bullet(self.arm_angle, self.arm_rect.center))
            self.bullet_timer = 20
        self.bullet_group.update()
        self.bullet_timer -= 1
        pygame.sprite.groupcollide(self.bullet_group, self.game.get_enemy_group(), True, True)

    def shoot_bullet(self) -> pygame.sprite.Sprite:
        return Bullet(self.arm_angle, self.arm_rect.center)
