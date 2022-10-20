import re
from pynput import keyboard

"""
The KeyboardListener class is a wrapper around a pynput listener.
It tracks the input of alphanumeric, punctuation, and space characters.
Additionally, it provides a word count of the number of words typed
since creation of the listener or last reset. 
"""
class KeyboardListener():

  def __init__(self):
    self._input = ""
    self._word_count = 0
    self.__listener = None
    self._enabled = False

  @property
  def input(self):
    return self._input

  @input.setter
  def input(self, input):
    self._input = input
  
  @property
  def word_count(self):
    return self._word_count

  @word_count.setter
  def word_count(self, word_counter):
    self._word_count = word_counter

  @property
  def enabled(self):
    return self._enabled

  @enabled.setter
  def enabled(self, enabled):
    self._enabled = enabled

  """
  Creates a new KeyboardListener
  """
  def create_listener(self):
    self.__listener = keyboard.Listener(
      on_press=self.__handle_key_press
    )

    self.__listener.start()
    self.enabled = True

  """
  Releases the KeyboardListener
  """
  def release_listener(self):
    self.__listener.stop()
    self.enabled = False

  """
  Resets the Keyboard Listener by clearing it input, resetting
  word count, and setting enabled to False.
  """
  def reset(self):
    self._input = ""
    self._word_count = 0
    self._enabled = False

  def __handle_key_press(self, key):
    if self.enabled:
      try:
        if key == keyboard.Key.space:
          self._input += " "
          self.__count_words()

        elif key == keyboard.Key.backspace:
          if len(self._input) > 0:
            self._input = self._input[:-1]
            self.__count_words()

        else:
          self._input += str(key.char)
          self.__count_words()

      except AttributeError:
        pass

  def __count_words(self):
    matches = re.findall("[\w-]+", self._input)
    self.word_count = len(matches)
