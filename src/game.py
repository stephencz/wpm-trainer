import sys
import pygame
from abc import ABC, abstractmethod

class Entity(ABC):
  
  def __init__(self):
    pass

  @abstractmethod
  def render(self):
    pass

  @abstractmethod
  def destroy(self):
    pass

class TimerEntity(Entity):
  
  def __init__(self):
    pass

  def render(self):
    pass

  def destroy(self):
    pass

class Game():

  def __init__(self):
    
    # Configure the window
    self._width = 480
    self._height = 360
    self._screen = pygame.display.set_mode((self._width, self._height))

    # Configure game clock
    self._clock = pygame.time.Clock()
    self._deltatime = 0

    # Entities
    self._entity_timer = TimerEntity()


  def loop(self):
    while True:
      self._deltatime = self._clock.tick(60)

      for event in pygame.event.get():
        self._handle_quit_event(event)
        self._handle_resize_event(event)

      self._screen.fill((255, 255, 255))
      self.render()

  def _handle_quit_event(self, event):
    if event.type == pygame.QUIT:
      self.close()

  def _handle_resize_event(self, event):
    if event.type == pygame.VIDEORESIZE:
      self._screen = pygame.display.set_mode((self._width, self._height))

  def render(self):
    self._entity_timer.render()


  def close(self):
    self._entity_timer.destroy()
    sys.exit()


game = Game()
game.loop()