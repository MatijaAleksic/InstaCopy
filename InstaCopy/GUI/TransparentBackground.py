#Import the Tkinter Library
from tkinter import *

#Create an instance of Tkinter Frame
win = Tk()

#Set the geometry of window
win.geometry("700x350")

#Add a background color to the Main Window
win.config(bg = '#add123')

#Create a transparent window
win.wm_attributes('-transparentcolor','#add123')
win.mainloop()