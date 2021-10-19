from tkinter import *

root = Tk()

c = Canvas(root)
c.pack()
c.create_rectangle(100, 100, 200, 200)

root.mainloop()