import pygame
from pygame.locals import *
import os


# Game Setup
pygame.init()
screen = pygame.display.set_mode((720, 960))
FPS = 60
clock = pygame.time.Clock()
game = True
current_work_dir = os.getcwd()
current_work_dir = current_work_dir[:-5]
os.chdir(current_work_dir)


class Player(pygame.sprite.Sprite):
    # this builds the player object
    # the player object holds the firing mechanism, listens to the game
    # for input, and tells the game the angle of the rod when it fires?
    # Like a getBulletPath function or something
    def __init__(self):
        super().__init__()
        self.tank_body = pygame.image.load("resources/images/tank_body.png")
        self.body_rect = self.tank_body.get_rect()
        self.body_rect.center = (360, 820)
        self.tank_arm = pygame.image.load("resources/images/tank_arm.png")
        self.arm_rect = self.tank_arm.get_rect()
        self.arm_rect.center = (360, 800)

    def draw(self, surface):
        surface.blit(self.tank_body, self.body_rect)
        surface.blit(self.tank_arm, self.arm_rect)

    def update(self, pressed):
        if pressed[K_RIGHT] and self.arm_rect.right < 720:
            # rotate arm (for now move to test)
            self.arm_rect.move_ip(5, 0)
        if pressed[K_LEFT] and self.arm_rect.left > 0:
            # rotate arm (for now move to test)
            self.arm_rect.move_ip(-5, 0)


P1 = Player()

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
    P1.draw(screen)

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
