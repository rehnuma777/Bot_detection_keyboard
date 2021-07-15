from pynput import keyboard
from pynput.keyboard import Listener
import time
import pandas as pd
import csv



#responsible for handling input streams like listening ot controlling
counter_time = 0


p = []
r = []
count = 0
keydata = 'a'
global key
filename = 'log.csv'
#def writetofile(key):

def write_headers():
    write_row('Key pressed','Key released','Time' )

def write_row(keypressed, keyrelease, time):
    with open(filename, 'a') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([keypressed,keyrelease,time])



def on_press(key):
        #try:
        global t
        keydata = str(key)

        keydata = keydata.replace("'","")
        counter_t = round(time.time()-t, 2)
        #p.append(counter_t)
        #time = keydata.time
        write_row(keydata,'', counter_t)
        

def  on_release(key):
    global t
    counter_time = 0
    counter_time = round(time.time()-t, 2)
    #r.append(counter_time)
    write_row(' ',key, counter_time)

     #print('{0} released'.format(key))
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
