from pynput import keyboard
from pynput.keyboard import Listener
import time
import pandas as pd
import csv

from datetime import datetime

#responsible for handling input streams like listening ot controlling
counter_time = 0

filename = datetime.now().strftime("%Y-%m-%d-%H-%M.csv")

p = []
r = []
count = 0
keydata = 'a'
kp_dict= {}
d = []
#t = time.time()
global key


def write_headers():
    write_row('Key pressed','Key released','Time', 'Hold time', 'Consecutive Press and Release')



def write_row(keypressed, keyreleased, timestamp,Hold_time,press_release):
    with open(filename, 'a') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([keypressed,keyreleased,timestamp,Hold_time, press_release])



def on_press(key):
        #try:
        global t
        keydata = str(key)
        keydata = keydata.replace("'","")
        pressed_t = round(time.time()-t, 2)
        kp_dict[keydata] = pressed_t
        write_row(keydata,'None', pressed_t,'', '')



def  on_release(key):
    global t
    keydata = str(key)
    keydata = keydata.replace("'","")
    released_time = 0
    released_time = round(time.time()-t, 2)
    r.append(released_time)
    time_val = list(kp_dict.values())
    zip_list = zip(list(kp_dict.values()),list(kp_dict.keys()))
    recent_pressed = sorted(time_val,reverse=True)
    up_up = recent_pressed[0]-recent_pressed[-1]
    if key not in kp_dict:
        press_time = kp_dict.pop(keydata)
    write_row('None',key, released_time,str(released_time-press_time), released_time-recent_pressed[0])


    if key == keyboard.Key.esc:
        # Stop listener
        return False



def start_program():
    global t
    t = time.time()
    write_headers()
    with Listener(on_press=on_press,on_release=on_release) as l:
        l.join()
        #count +=1
