import sys, pygame
from abc import ABC, abstractmethod
from screen import GameScreen
from entity import TimerEntity

"""
The Game class creates a window and can manage scenes.
"""
class Game():

  def __init__(self):
    
    pygame.font.init()

    # Configure the window
    self._should_destroy = False

    self._width = 480
    self._height = 360
    self._display = pygame.display.set_mode((self._width, self._height))

    # Configure game clock
    self._clock = pygame.time.Clock()
    self._deltatime = 0

    self._screen = GameScreen(self)

  def loop(self):
    while not self._should_destroy:
      self._deltatime = self._clock.tick(30)

      self._screen.logic(self._deltatime)
      self._screen.render(self._deltatime)

    self.destroy()

  def set_screen(self, screen):
    self._screen.destroy()
    self._screen = screen

  def destroy(self):
    self._screen.destroy()
    sys.exit()
