import tkinter as tk
from tkinter import *
import threading
import key as k


bg = "light sky blue"
global window

def gui():

    window = tk.Tk()
    window.geometry("800x800")
    window.title("Keystroke")
    greeting = tk.Label(window, text="Bot or Not?",font = 'Helvetica 16 italic')
    greeting.pack()
    greeting1 = tk.Label(window, text="INSTRUCTIONS: 1. Click on capture 2. Type the words below for 10 times each \n\n")
    greeting1.pack()
    lable1 = Label(window, text='101AAPBajk!').pack()
    entry = tk.Text(window,height =10, width=40,padx=40, pady=40)
    entry.pack(pady=20)
    lable2 = Label(window, text="123ABCabc!").pack()
    entry1 = tk.Text(window, height =10, width=40,padx= 40, pady = 40)
    entry1.pack(pady=20)
    b1 = Button(window, text = "Capture",bg=bg, font ='Verdana 16 italic', command = start).pack(side=LEFT)
    b2 = Button(window, text = "Exit",bg=bg,font='Verdana 16 italic', command = window.destroy).pack(side=RIGHT)
    window.mainloop()
    window.after(5, start)


def start():
 t1 = threading.Thread(target=k.start_program).start()

if __name__ =="__main__":
    gui()
