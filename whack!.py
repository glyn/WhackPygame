import sys
import time

import pygame

from settings import Settings
from mole import Mole
from game_stats import GameStats
from scoreboard import Scoreboard
from cloud import Cloud

import random


def _seconds_since_epoch():
    return time.mktime(time.localtime())


class Whack:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats(self)

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.cloud = Cloud(self)
        self.cloud.rect.x = 200
        self.cloud.rect.y = 0

        self.image = pygame.image.load("images/grass.png")
        self.rect = self.image.get_rect()

        self.sb = Scoreboard(self)
        self.moles = [Mole(self) for i in range(9)]
        x_values = [25, 200, 375]
        y_values = [0, 175, 350]
        for i in range(0, 9):
            mole = Mole(self)
            mole.rect.x = x_values[i % 3]
            mole.rect.y = y_values[i // 3]
            self.moles[i] = mole

        self.timer = 0.0
        self.mole_timer = 0.0
        self.selectedMole = 0
        self.making_alpha = False
        self.making_visible = False
        self.time_since_last_mole = _seconds_since_epoch()

    # Draw a solid blue circle in the center

    def print_moles(self):
        for mole in self.moles:
            mole.blitme()

    def print_cloud(self):
        self.cloud.blitme()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def _update_screen(self):
        self.blitme()
        self.print_moles()
        self.sb.show_score()

        # Flip the display
        pygame.display.flip()

    def _check_mole(self, mouse_pos):
        for mole in self.moles:
            mole_clicked = mole.rect.collidepoint(mouse_pos)
            if mole_clicked and mole.is_alive():
            # Increase score once and then clear the mole
                self.stats.score += self.settings.mole_points
                self.sb.prep_score()
                mole.clear()
                break

    def _make_mole_alive(self):
        # Randomly picks a mole to spawn
        self.selectedMole = random.randint(0, 8)
        # Time since spawn
        self.moles[self.selectedMole].m_time = _seconds_since_epoch()
        self.moles[self.selectedMole].alive = True
        if self.moles[self.selectedMole].is_alive:
            self.moles[self.selectedMole].image = pygame.image.load("images/mole.png")

    def _check_events(self):
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_mole(mouse_pos)

    def run_game(self):
        self._make_mole_alive()
        self.stats.reset_stats()
        self.settings.initialise_dynamic_settings()
        while True:
            self._check_events()

            current_time = _seconds_since_epoch()

            # Spawn a mole every second
            if current_time - self.time_since_last_mole >= 1.0:
                self._make_mole_alive()
                self.time_since_last_mole = current_time

             # Clear old moles
            for mole in self.moles:
                random_time = random.randint(4, 6)
                if current_time - mole.m_time >= random_time:
                    mole.clear()
                    self.stats.score - self.settings.mole_points
                    self.sb.prep_score()

            self._update_screen()
        # Done! Time to quit.
        pygame.quit()


if __name__ == '__main__':
    w = Whack()
    w.run_game()
