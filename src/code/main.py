import math

import pygame
from pygame.locals import *
import os
from math import sin, cos
from random import randint


# Game Setup
pygame.init()
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 960
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60
clock = pygame.time.Clock()
game = True
current_work_dir = os.getcwd()
current_work_dir = current_work_dir[:-5]
os.chdir(current_work_dir)


class Game(pygame.sprite.Sprite):
    # Needed just for collisions with parachuters
    def __init__(self, width, height):
        super().__init__()
        self.ground = pygame.Surface([width, height])
        self.ground.fill("green")
        self.rect = self.ground.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT))
        self.paused = False
        self.player = Player()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_timer = 0
        self.enemy_timer = 0

    def draw(self, surface):
        surface.blit(self.ground, self.rect)
        self.player.draw(surface)
        self.bullet_group.draw(surface)
        self.enemy_group.draw(surface)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_p]:
            self.paused = not self.paused
        if not self.paused:
            if pressed_keys[K_SPACE] and self.bullet_timer <= 0:
                self.bullet_group.add(self.player.shoot_bullet())
                self.bullet_timer = 20
            self.player.update(pressed_keys)
            self.bullet_group.update()
            self.bullet_timer -= 1

            #need proper enemy factory but rn just want consistency for testing
            if self.enemy_timer == 0:
                self.enemy_timer = 100
                self.enemy_group.add(Enemy(randint(0, SCREEN_WIDTH)))
            self.enemy_group.update()
            self.enemy_timer -= 1


class Player(pygame.sprite.Sprite):
    # this builds the player object
    # the player object holds the firing mechanism, listens to the game
    # for input, and tells the game the angle of the rod when it fires?
    # Like a getBulletPath function or something
    def __init__(self):
        super().__init__()
        self.tank_body = pygame.image.load("resources/images/tank_body.png")
        self.body_rect = self.tank_body.get_rect(center=(SCREEN_WIDTH/2, 820))
        self.draw_body = self.tank_body
        self.draw_body_rectangle = self.body_rect
        self.tank_arm = pygame.image.load("resources/images/tank_arm.png")
        self.arm_rect = self.tank_arm.get_rect(center=(SCREEN_WIDTH/2, 810))
        self.draw_arm = self.tank_arm
        self.draw_arm_rectangle = self.arm_rect
        self.arm_angle = 0
        self.bullet_group = pygame.sprite.Group()

    def draw(self, surface):
        surface.blit(self.draw_body, self.draw_body_rectangle)
        surface.blit(self.draw_arm, self.draw_arm_rectangle)

    def update(self, pressed):
        # want to use match - case here but need to learn more about pressed first
        if pressed[K_RIGHT] and self.arm_angle > -90:
            self.arm_angle -= 1
            self.draw_arm = pygame.transform.rotate(self.tank_arm, self.arm_angle)
        if pressed[K_LEFT] and self.arm_angle < 90:
            self.arm_angle += 1
            self.draw_arm = pygame.transform.rotate(self.tank_arm, self.arm_angle)
        self.draw_arm_rectangle = self.draw_arm.get_rect(center=self.arm_rect.center)

    def shoot_bullet(self) -> pygame.sprite.Sprite:
        return Bullet(self.arm_angle, self.arm_rect.center)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, arm_center):
        super().__init__()
        self.collision = False
        self.bullet_image = pygame.image.load("resources/images/bullet.png")
        self.image = pygame.transform.scale_by(self.bullet_image, 0.5)
        self.rect = self.image.get_rect(center=arm_center)
        self.angle = angle
        x, y = arm_center
        self.delta_x = sin(math.radians(-angle))
        self.delta_y = cos(math.radians(-angle))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect.move_ip(40*self.delta_x, -40*self.delta_y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip(4*self.delta_x, -4*self.delta_y)
        if self.rect.top < 0 or self.rect.left < 0 or self.rect.right > 720:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.image.load("resources/images/soldier.png")
        self.rect = self.image.get_rect(center=(location, -40))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip(0, 1)


_game = Game(720, 260)

# Game Loop
while game:
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False

    _game.update()
    screen.fill("blue")
    _game.draw(screen)

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
