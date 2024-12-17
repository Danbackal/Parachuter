import math

import pygame
from pygame.locals import *
import os
from math import sin, cos
from random import randint


SCREEN_WIDTH = 720
SCREEN_HEIGHT = 960
FPS = 60


class Game(pygame.sprite.Sprite):
    # Owns the game and game state
    def __init__(self):
        super().__init__()
        self._game_start = 1
        self._game_running = 2
        self._game_paused = 3
        self._game_end = 4
        self._game_close = 5
        self.GAME_STATE = self._game_start
        self.ground = pygame.Rect(0, 830, SCREEN_WIDTH, 130)
        self.paused = False
        self.player = Player()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_timer = 0

    def draw(self, surface):
        # surface.blit(self.ground, self.rect)
        pygame.draw.rect(surface, "green", self.ground)
        self.player.draw(surface)
        self.enemy_group.draw(surface)

    def update(self):
        # GAME STATE OPTIONS:
        # START - will have start menu. Can only play or close
        # GAME - running game. Will continue game loop and updates. Can only pause or finish
        # PAUSE - pause menu. Can unpause, restart, or quit. Restart will either set back to START or just reset values
        # END - end game. Can restart or close.
        # CLOSE - closes the game
        match self.GAME_STATE:
            case self._game_start:
                self.GAME_STATE = self._game_running
            case self._game_running:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_p]:
                    self.GAME_STATE = self._game_paused
                self.player.update(pressed_keys)

                #need proper enemy factory but rn just want consistency for testing
                if self.enemy_timer == 0:
                    self.enemy_timer = 100
                    self.enemy_group.add(Enemy(randint(0, SCREEN_WIDTH)))
                self.enemy_group.update()
                self.enemy_timer -= 1
            case self._game_paused:
                print("Game State set to Paused")
            case self._game_end:
                print("Game State set to End")
                # Temp set to paused just for verification
                self.GAME_STATE = self._game_paused
            case self._game_close:
                print("Game State set to Close")

    def get_enemy_group(self):
        return self.enemy_group

    def get_game_state(self):
        return self.GAME_STATE

    def set_game_close(self):
        self.GAME_STATE = self._game_close

    def set_game_end(self):
        self.GAME_STATE = self._game_end

    def get_ground_rect(self):
        return self.ground

    def run(self):
        return self.GAME_STATE != self._game_close


class Player(pygame.sprite.Sprite):
    # Owns the player tank, as well as the bullets shot from the tank
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
        pygame.sprite.groupcollide(self.bullet_group, _game.get_enemy_group(), True, True)

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
        if self.rect.colliderect(_game.get_ground_rect()):
            _game.set_game_end()


# Game Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
current_work_dir = os.getcwd()
current_work_dir = current_work_dir[:-5]
os.chdir(current_work_dir)
_game = Game()

# Game Loop
# To Add:
# Game State - start, running, paused, finished, and closed. Closed will end the game loop
# Game menu - start menu, pause menu (resume, quit, or restart), finish menu (quit or restart)
while _game.run():
    for event in pygame.event.get():
        if event.type == QUIT:
            _game.set_game_close()

    _game.update()
    screen.fill("blue")
    _game.draw(screen)

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
