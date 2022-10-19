import sys, pygame
from tokenize import Number
from pygame.sprite import Sprite
from abc import ABC, abstractmethod


class EntityManager():

  def __init__(self):
    self._entities = []

  def add(self, entity):
    self._entities.append(entity)

  @property
  def entities(self):
    return self._entities

  @entities.setter
  def entities(self, entities):
    self._entities = entities

"""
The Entity abstract base class provides the interface that 
all screens shouold implement.
"""
class Entity(ABC):
  
  def __init__(self, game, x=0, y=0):
    self._game = game
    self._x = x
    self._y = y

  @abstractmethod
  def logic(self, deltatime):
    pass

  @abstractmethod
  def render(self, deltatime):
    pass

  @abstractmethod
  def destroy(self):
    pass

  @property
  def x(self):
    return self._x

  @x.setter
  def x(self, x):
    self._x = x

  @property
  def y(self):
    return self._y

  @y.setter
  def y(self, y):
    self._y = y

class NumberTrackerMinusSprite(Sprite):

  def __init__(self, x, y):
    Sprite.__init__(self)
    self._rect = pygame.Rect(x, y, 34, 32)
    self._image = pygame.image.load("assets/tracker_minus.png")

  def update(self):
    pass

class NumberTrackerPlusSprite(Sprite):

  def __init__(self, x, y):
    Sprite.__init__(self)
    self._rect = pygame.Rect(x, y, 64, 32)
    self._image = pygame.image.load("assets/tracker_plus.png")

  def update(self):
    pass

class NumberTrackerBarSprite(Sprite):

  def __init__(self, x, y):
    Sprite.__init__(self)
    self._rect = pygame.Rect(x, y, 34, 32)
    self._image = pygame.image.load("assets/tracker_bar.png")

  def update(self):
    pass

class NumberTrackerEntity(Entity):

  def __init__(self, game, min, max, value, label, x=0, y=0):
    Entity.__init__(self, game, x, y)

    self._min = min
    self._max = max
    self._value = value

    self._font = pygame.font.SysFont('Comic sans MS', 16)
    self._label = self._font.render(label, False, (0, 0, 0))
    self._bar_contents = self._font.render(str(self._value), False, (255, 255, 255))

    self._minus_sprite = NumberTrackerMinusSprite(self._x, self._y)
    self._bar_sprite = NumberTrackerBarSprite(self._x + 36, self._y)
    self._plus_sprite = NumberTrackerPlusSprite(self._x + 102, self._y)


  def logic(self, deltatime):
    self._minus_sprite.update()
    self._plus_sprite.update()
    self._bar_sprite.update()

  def render(self, deltatime):
    self._game._display.blit(self._label, (self._x, self._y - 26))
    self._game._display.blit(self._minus_sprite._image, self._minus_sprite._rect)
    self._game._display.blit(self._bar_sprite._image, self._bar_sprite._rect)
    self._game._display.blit(self._plus_sprite._image, self._plus_sprite._rect)
    self._game._display.blit(self._bar_contents, (self._x + 50, self._y + 5))

  def destroy(self):
    pass

class TargetWPMTrackerEntity(NumberTrackerEntity):

  def __init__(self, game, x, y):
    NumberTrackerEntity.__init__(self, game, 1, 200, 25, 'Words Per Minute', x, y)

  def logic(self, deltatime):
    super().logic(deltatime)
  


  def render(self, deltatime):
    super().render(deltatime)

  def destroy(self):
    pass

class TargetTimeTrackerEntity(NumberTrackerEntity):

  def __init__(self, game, x, y):
    NumberTrackerEntity.__init__(self, game, 1, 60, 60, 'Minutes Per Session', x, y)

  def logic(self, deltatime):
    super().logic(deltatime)

  def render(self, deltatime):
    super().render(deltatime)

  def destroy(self):
    pass

class TimerEntity(Entity):
  
  def __init__(self, game):
    Entity.__init__(self, game)

  def logic(self, deltatime):
    pass

  def render(self, deltatime):
    pass

  def destroy(self):
    pass