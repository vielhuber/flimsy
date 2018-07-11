import keyboard
import pyperclip
from time import sleep
from pymouse import PyMouse
from pykeyboard import PyKeyboard

recorded = keyboard.record(until='esc')

print(list(keyboard.get_typed_strings(recorded)))