import sys, pygame
from abc import ABC, abstractmethod


"""
The Entity abstract base class provides the interface that 
all screens shouold implement.
"""
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