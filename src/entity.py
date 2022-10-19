import sys, pygame
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
  
  def __init__(self):
    pass

  @abstractmethod
  def logic(self, deltatime):
    pass

  @abstractmethod
  def render(self, deltatime):
    pass

  @abstractmethod
  def destroy(self):
    pass


class DropDownEntity(Entity):

  def __init__(self):
    pass

  def logic(self, deltatime):
    pass

  def render(self, deltatime):
    pass

  def destroy(self):
    pass

class TimerEntity(Entity):
  
  def __init__(self):
    pass

  def logic(self, deltatime):
    pass

  def render(self, deltatime):
    pass

  def destroy(self):
    pass