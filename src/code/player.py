from bullet import Bullet
import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    # Owns the player tank, as well as the bullets shot from the tank
    def __init__(self, game, font):
        super().__init__()
        self.game = game
        self.font = font
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
        self.bullets = 100
        self.bullet_location = (20, 10)
        self.bullet_board = self.font.render("Bullets: {}".format(str(self.bullets)), True, "black")
        self.bullet_rect = self.bullet_board.get_rect(topleft=self.bullet_location)
        self.shot = 0
        self.reload = 1
        self.reset = 2
        self.money = 0
        self.money_location = (20, 35)
        self.money_board = self.font.render("Money: {}".format(str(self.money)), True, "black")
        self.money_rect = self.money_board.get_rect(topleft=self.money_location)
        self.enemy_value = 10

    def draw(self, surface):
        surface.blit(self.draw_arm, self.draw_arm_rectangle)
        surface.blit(self.draw_body, self.draw_body_rectangle)
        self.bullet_group.draw(surface)

    def draw_player_header(self, surface):
        surface.blit(self.bullet_board, self.bullet_rect)
        surface.blit(self.money_board, self.money_rect)

    def update(self, pressed):
        # want to use match - case here but need to learn more about pressed first
        if pressed[K_RIGHT] and self.arm_angle > -90:
            self.arm_angle -= 1.5
            self.draw_arm = pygame.transform.rotate(self.tank_arm, self.arm_angle)
        if pressed[K_LEFT] and self.arm_angle < 90:
            self.arm_angle += 1.5
            self.draw_arm = pygame.transform.rotate(self.tank_arm, self.arm_angle)
        self.draw_arm_rectangle = self.draw_arm.get_rect(center=self.arm_rect.center)
        if pressed[K_SPACE] and self.bullet_timer <= 0 < self.bullets:
            self.update_bullet_count(self.shot)
            self.bullet_group.add(Bullet(self.arm_angle, self.arm_rect.center))
            self.bullet_timer = 15
        self.bullet_group.update()
        self.bullet_timer -= 1
        # mask instead of rectangle collision for better hit marks. In bigger games,
        # can do rectangle without dokill first. This is less intensive. If rectangle collision,
        # check for mask collision.
        # That might need to be done in the update function of the bullet though, and not in the player
        # Worth considering a redesign where all classes have access to the game, and game functions, directly
        if pygame.sprite.groupcollide(self.bullet_group, self.game.get_enemy_group(), True, True, pygame.sprite.collide_mask):
            self.game.update_scoreboard(0)
            self.update_money(self.enemy_value)

    def update_bullet_count(self, update):
        match update:
            case self.shot:
                self.bullets -= 1
            case self.reload:
                self.bullets += 100
            case self.reset:
                self.bullets = 100
        self.bullet_board = self.font.render("Bullets: {}".format(str(self.bullets)), True, "black")
        self.bullet_rect = self.bullet_board.get_rect(topleft=self.bullet_location)

    def update_money(self, update):
        self.money += update
        self.money_board = self.font.render("Money: {}".format(str(self.money)), True, "black")
        self.money_rect = self.money_board.get_rect(topleft=self.money_location)

    def reset_game(self):
        self.bullet_group.empty()
        self.arm_angle = 0
        # self.draw_arm = pygame.transform.rotate(self.tank_arm, self.arm_angle)
        self.draw_arm = self.tank_arm
        self.draw_arm_rectangle = self.arm_rect
        self.update_bullet_count(self.reset)
        self.update_money(-self.money)
