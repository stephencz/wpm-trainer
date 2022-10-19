import pygame
from enum import Enum
from abc import ABC, abstractmethod
from entity import EntityManager
from entity import TimerEntity
from entity import TargetWPMTrackerEntity
from entity import TargetTimeTrackerEntity
from keyboard import KeyboardListener

class SessionState(Enum):
  INIT    = 1
  RUNNING = 2
  PAUSED  = 3
  END     = 4

"""
The Screen abstract base class provides the interface that
all screens should implement.
"""
class Screen(ABC):

  def __init__(self, game):
    self._game = game

  @abstractmethod
  def logic(self, deltatime):
    pass

  @abstractmethod
  def render(self, deltatime):
    pass

  @abstractmethod
  def destroy(self):
    pass


"""
The main gameplay screen
"""
class GameScreen(Screen):

  def __init__(self, game):
    Screen.__init__(self, game)

    # Configure Game Data
    self._keyboard_listener = KeyboardListener() 
    self._session_state = SessionState.INIT
    self._target_wpm = 25         
    self._target_time = 60

    # Entities
    self._entity_manager = EntityManager()
    self._entity_wpm_tracker = TargetWPMTrackerEntity(self._game, 30, 30)
    self._entity_time_tracker = TargetTimeTrackerEntity(self._game, 190, 30)
    self._entity_timer = TimerEntity(self._game)

    self._entity_manager.add(self._entity_timer)
    self._entity_manager.add(self._entity_wpm_tracker)
    self._entity_manager.add(self._entity_time_tracker)

  def logic(self, deltatime):
    for event in pygame.event.get():
      self._handle_quit_event(event)
      self._handle_resize_event(event)  

    for entity in self._entity_manager.entities:
      entity.logic(deltatime)

  def _handle_quit_event(self, event):
    if event.type == pygame.QUIT:
      self.destroy()

  def _handle_resize_event(self, event):
    if event.type == pygame.VIDEORESIZE:
      self._game._display = pygame.display.set_mode((self._width, self._height))

  def render(self, deltatime):
    self._game._display.fill((255, 255, 255))
    
    for entity in self._entity_manager.entities:
      entity.render(deltatime)

    pygame.display.flip()

  def destroy(self):
    self._game._should_destroy = True

    for entity in self._entity_manager.entities:
      entity.destroy()