from tkinter import *
import sys
from pyscreenshot import grab
from util import *


class InstaCopy():
    def __init__(self):

        self.selectedPoint = None
        self.rect = None

        # pronalazenje rezolucije ekrana
        [self.width, self.height] = get_resolution()

        # podesavanje main window-a
        self.master = Tk(className='InstaCopy')
        # drugi window
        self.select_window = Canvas(self.master, width=self.width, height=self.height, bg='red')

    def run(self):
        # podesavanje fullscreena
        self.master.attributes('-fullscreen', True)

        # podesavanje transparencije
        self.master.attributes('-alpha', 0.1)

        # bindujemo escape za izlazak
        self.master.bind('<Escape>', self.close)

        # bindujemo enter za screenshot
        self.master.bind('q', self.take_screenshot)

        # dodavanje background frame koji ce da cita sta se desava na ekranu

        # events
        self.select_window.bind('<B1-Motion>', self.motion)  # da se binduje za motion ovaj frame
        self.select_window.bind('<Button>', self.first_click)
        self.select_window.bind('<ButtonRelease>', self.release)

        self.select_window.pack()

        # master.withdraw()
        mainloop()

    # funcija eventa za pracenje pomeranje misa
    def motion(self, event):
        print(event)
        #print("Mouse position: (%s %s)" % (event.x, event.y))

        if self.selectedPoint is not None:
            #print(f"{self.selectedPoint[0]}  {self.selectedPoint[1]}  {event.x}  {event.y}")
            #self.rect = self.select_window.create_rectangle(self.selectedPoint[0],self.selectedPoint[1], event.x, event.y, fill="black")
            self.select_window.coords(self.rect, self.selectedPoint[0], self.selectedPoint[1], event.x, event.y)
            #self.select_window.
        return

    def close(self, event):
        self.master.withdraw()  # if you want to bring it back
        sys.exit()  # if you want to exit the entire thing

    def take_screenshot(self, point1, point2):
        print("SLIKATI")
        #print(point1, point2)
        im = grab(bbox=(point1[0], point1[1], point2[0], point2[1]))
        im.save("Screenshot.jpg")
        # im.show()

        #self.master.withdraw()  # if you want to bring it back
        #sys.exit()  # if you want to exit the entire thing

    def first_click(self, event):
        #print("Mouse position: (%s %s)" % (event.x, event.y))
        self.selectedPoint = [event.x, event.y]
        self.rect = self.select_window.create_rectangle(self.selectedPoint[0],self.selectedPoint[1], self.selectedPoint[0], self.selectedPoint[1], fill="black")

        return

    def release(self, event):
        #print("Mouse position: (%s %s)" % (event.x, event.y))

        screen_shot_rectangle = [self.selectedPoint[0], self.selectedPoint[1], event.x, event.y]
        #print(f"{screen_shot_rectangle[0]} {screen_shot_rectangle[1]} {screen_shot_rectangle[2]} {screen_shot_rectangle[3]} ")

        if screen_shot_rectangle[0] > screen_shot_rectangle[2]:
            temp = screen_shot_rectangle[0]
            screen_shot_rectangle[0] = screen_shot_rectangle[2]
            screen_shot_rectangle[2] = temp

        if screen_shot_rectangle[1] > screen_shot_rectangle[3]:
            temp = screen_shot_rectangle[1]
            screen_shot_rectangle[1] = screen_shot_rectangle[3]
            screen_shot_rectangle[3] = temp

        self.select_window.delete(self.rect)
        self.take_screenshot([screen_shot_rectangle[0],screen_shot_rectangle[1]], [screen_shot_rectangle[2],screen_shot_rectangle[3]])
        self.selectedPoint = None
        self.rect = None
        return


InstaCopy().run()
