import pygame
from pygame.locals import *
import os

from player import Player
from enemy import Enemy
from button import Button


class Game(pygame.sprite.Sprite):
    # Owns the game and game state
    def __init__(self, width, height):
        super().__init__()
        self._game_start = 1
        self._game_running = 2
        self._game_paused = 3
        self._game_end = 4
        self._game_close = 5
        self._game_width = width
        self._game_height = height
        self._game_fps = 60
        self.GAME_STATE = self._game_start
        self.start_button = Button(self, "start")
        self.start_button.set_center(self._game_width/2, self._game_height/2)
        self.resume_button = Button(self, "resume")
        self.restart_button = Button(self, "restart")
        self.quit_button = Button(self, "quit")
        self.state_change = False
        self.ground = pygame.Rect(0, 830, self._game_width, 130)
        self.pause_menu_background = pygame.Surface((self._game_width, self._game_height))
        self.pause_menu_background.set_alpha(135)
        self.pause_menu_background.fill("grey")
        self.paused = False
        self.player = Player(self)
        self.enemy_group = pygame.sprite.Group()
        self.enemy_timer = 0

    def draw(self, surface):
        # surface.blit(self.ground, self.rect)
        pygame.draw.rect(surface, "green", self.ground)
        self.player.draw(surface)
        self.enemy_group.draw(surface)
        # Based on game state - draw surfaces overtop the above
        match self.GAME_STATE:
            case self._game_start:
                self.start_button.draw(surface)
            case self._game_paused:
                surface.blit(self.pause_menu_background, (0, 0))
                self.resume_button.draw(surface)
                self.restart_button.draw(surface)
                self.quit_button.draw(surface)
            case self._game_end:
                self.restart_button.draw(surface)
                self.quit_button.draw(surface)
                print("end draw")

    def update(self):
        # GAME STATE OPTIONS:
        # START - will have start menu. Can only play or close
        # GAME - running game. Will continue game loop and updates. Can only pause or finish
        # PAUSE - pause menu. Can unpause, restart, or quit. Restart will either set back to START or just reset values
        # END - end game. Can restart or close.
        # CLOSE - closes the game
        pressed_keys = pygame.key.get_pressed()
        match self.GAME_STATE:
            case self._game_start:
                if self.state_change:
                    pygame.mouse.set_visible(True)
                    self.start_button.set_center(self._game_width / 2, self._game_height / 2)
                    self.state_change = False
                if pygame.mouse.get_pressed():
                    if self.start_button.check_click(pygame.mouse.get_pos()):
                        self.GAME_STATE = self._game_running
                        self.state_change = True

            case self._game_running:
                if self.state_change:
                    pygame.mouse.set_visible(False)
                    self.state_change = False
                if pressed_keys[K_p]:
                    self.GAME_STATE = self._game_paused
                    self.state_change = True
                self.player.update(pressed_keys)
                #need proper enemy factory but rn just want consistency for testing
                if self.enemy_timer == 0:
                    self.enemy_timer = 100
                    self.enemy_group.add(Enemy(self))
                self.enemy_group.update()
                self.enemy_timer -= 1

            case self._game_paused:
                if self.state_change:
                    pygame.mouse.set_visible(True)
                    self.resume_button.set_center(self._game_width / 2, self._game_height / 2 - 95)
                    self.restart_button.set_center(self._game_width / 2, self._game_height / 2)
                    self.quit_button.set_center(self._game_width / 2, self._game_height / 2 + 95)
                    self.state_change = False
                if pygame.mouse.get_pressed():
                    if self.resume_button.check_click(pygame.mouse.get_pos()):
                        self.GAME_STATE = self._game_running
                        self.state_change = True
                    if self.restart_button.check_click(pygame.mouse.get_pos()):
                        self.GAME_STATE = self._game_start
                        self.state_change = True
                    if self.quit_button.check_click(pygame.mouse.get_pos()):
                        self.GAME_STATE = self._game_close
                        self.state_change = True

            case self._game_end:
                if self.state_change:
                    pygame.mouse.set_visible(True)
                    self.restart_button.set_center(self._game_width / 2, self._game_height / 2 - 60)
                    self.quit_button.set_center(self._game_width / 2, self._game_height / 2 + 60)
                    self.state_change = False
                if pygame.mouse.get_pressed():
                    if self.restart_button.check_click(pygame.mouse.get_pos()):
                        self.GAME_STATE = self._game_start
                        self.state_change = True
                    if self.quit_button.check_click(pygame.mouse.get_pos()):
                        self.GAME_STATE = self._game_close
                        self.state_change = True

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

    def game_width(self):
        return self._game_width

    def game_height(self):
        return self._game_height

    def get_frame_speed(self):
        return self._game_fps


# Game Setup
current_work_dir = os.getcwd()
current_work_dir = current_work_dir[:-5]
os.chdir(current_work_dir)
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 960
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)


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
    clock.tick(_game.get_frame_speed())


pygame.quit()
