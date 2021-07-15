import tkinter as tk
from tkinter import messagebox
from tkinter import *
import threading
import key as k
import sys



bg = "SlateGray1"
wr = []
global window

def gui():
    bound =10
    window = tk.Tk()
    window.geometry("800x400")
    window.title("Keystroke")
    greeting = tk.Label(window, text="BOT OR NOT?",font = 'Helvetica 16 bold', bg=bg)
    greeting.pack()
    greeting1 = tk.Label(window, text="Press Capture and type the following word 10 times", font = "Arial 14 bold", fg='orange2', bg=bg)
    greeting1.pack()
    def test(e):
        text = e.widget.get("1.0", "end-1c")

        new = len(text.split())
        print(new)
        if new > 3:
            terminate()

    lable2 = Label(window, text="123CAPabc!",bg=bg, font = 'Verdana 14 italic').pack()
    entry1 = tk.Text(window, height =10, width=40, pady=40, padx=40)
    entry1.pack(pady=20)
    entry1.bind('<KeyRelease>', test)
    #test = entry1.get("1.0", "end")
    #b2 = Button(window, text = "Test",bg='lightgoldenrod' , font='Helvetica 12 italic', command = retrieve_input).pack()
    b1 = Button(window, text = "Capture",bg='lightgoldenrod' , font='Helvetica 12 italic', command = start)
    b1.pack(side=LEFT)
    b2 = Button(window, text = "Exit",bg='lightgoldenrod',font='Helvetica 12 italic', command = terminate).pack(side=RIGHT)
    window.configure(bg=bg)
    window.mainloop()
    window.after(5, start)

def start():
 t1 = threading.Thread(target=k.start_program)
 t1.daemon = True
 t1.start()

def w_t():
  t2 = threading.Thread(target=w)
  #daemon thread allows to exit the main program even if the thread is running
  t2.daemon = True
  t2.start()
def terminate():
    sys.exit(0)

if __name__ =="__main__":
    gui()
