import pyautogui
import time
import random

text = "123ABCabc!"
length = len(text)
seconds = random.uniform(1,3)
pyautogui.typewrite(text, interval= seconds)
#time.sleep(1)
