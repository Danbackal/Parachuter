import pygame
from pygame.locals import *
import os
from math import sin, cos


# Game Setup
pygame.init()
screen = pygame.display.set_mode((720, 960))
FPS = 60
clock = pygame.time.Clock()
game = True
current_work_dir = os.getcwd()
current_work_dir = current_work_dir[:-5]
os.chdir(current_work_dir)


class Ground(pygame.sprite.Sprite):
    # Needed just for collisions with parachuters
    def __init__(self, width, height):
        super().__init__()
        self.ground = pygame.Surface([width, height])
        self.ground.fill("green")
        self.rect = self.ground.get_rect(center=(360, 960))

    def draw(self, surface):
        surface.blit(self.ground, self.rect)


class Player(pygame.sprite.Sprite):
    # this builds the player object
    # the player object holds the firing mechanism, listens to the game
    # for input, and tells the game the angle of the rod when it fires?
    # Like a getBulletPath function or something
    def __init__(self):
        super().__init__()
        self.tank_body = pygame.image.load("resources/images/tank_body.png")
        self.body_rect = self.tank_body.get_rect(center=(360, 820))
        self.draw_body = self.tank_body
        self.draw_body_rectangle = self.body_rect
        self.tank_arm = pygame.image.load("resources/images/tank_arm.png")
        self.arm_rect = self.tank_arm.get_rect(center=(360, 800))
        self.draw_arm = self.tank_arm
        self.draw_arm_rectangle = self.arm_rect
        self.arm_angle = 0
        self.pivot_length = 15 # approx

    def draw(self, surface):
        surface.blit(self.draw_body, self.draw_body_rectangle)
        surface.blit(self.draw_arm, self.draw_arm_rectangle)

    def update(self, pressed):
        # so to rotate around center, we need to store center of image as a pivot
        # get the rectangle of the rotated image with the same center
        # then add.

        # to get swivel arm, we need to figure out distance to center,
        # and then find the new center of the rotated object - pivot, angle, and distance
        # need center - y, where y is the height difference from center to pivot
        if pressed[K_RIGHT] and self.arm_angle > -90:
            self.arm_angle -= 1
            self.draw_arm = pygame.transform.rotate(self.tank_arm, self.arm_angle)
        if pressed[K_LEFT] and self.arm_angle < 90:
            self.arm_angle += 1
            self.draw_arm = pygame.transform.rotate(self.tank_arm, self.arm_angle)
        self.get_center()

    def get_center(self):
        (x, y) = self.arm_rect.center
        delta_x = self.pivot_length * sin(self.arm_angle)
        delta_y = self.pivot_length * cos(self.arm_angle)
        self.draw_arm_rectangle = self.draw_arm.get_rect(center=(x+delta_x, y+delta_y))


P1 = Player()
G1 = Ground(720, 260)
# We want a sprite Group to handle enemies, move all of them down at once, should
# handle listener style vibes


# Game Loop
while game:
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_SPACE]:
        # we fire the gun
        continue
    else:
        # for now, ignore things like pause
        P1.update(pressed_keys)

    screen.fill("blue")
    G1.draw(screen)
    P1.draw(screen)

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
