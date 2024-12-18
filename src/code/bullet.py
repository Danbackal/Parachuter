import pygame
from math import sin, cos, radians


class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, arm_center):
        super().__init__()
        self.collision = False
        self.bullet_image = pygame.image.load("resources/images/bullet.png")
        self.image = pygame.transform.scale_by(self.bullet_image, 0.5)
        self.rect = self.image.get_rect(center=arm_center)
        self.angle = angle
        x, y = arm_center
        self.delta_x = sin(radians(-angle))
        self.delta_y = cos(radians(-angle))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect.move_ip(35*self.delta_x, -35*self.delta_y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip(8*self.delta_x, -8*self.delta_y)
        if self.rect.top < 0 or self.rect.left < 0 or self.rect.right > 720:
            self.kill()
