#Import the library
from tkinter import *

#Create an instance of window
win= Tk()

#Set the geometry of the window
win.geometry("700x400")

def disable_button():
    win.destroy()
#Create a Label
Label(win,text="Type Something",font=('Helvetica bold', 25),
      fg="green").pack(pady=20)

#Create a Text widget
text= Text(win, height= 10,width= 40)
text.pack()

#Create a Disable Button
Button(win, text= "Quit", command= disable_button,fg= "white",
       bg="black", width= 20).pack(pady=20)

#win.withdraw()
win.mainloop()