from tkinter import *
import sys
from pyscreenshot import grab
from util import *

import pytesseract as tess
from PIL import Image

import clipboard

from pystray import MenuItem as item
import pystray

import threading

ctypes.windll.shcore.SetProcessDpiAwareness(2)

class InstaCopy():
    def __init__(self):


        self.master = Tk(className='InstantCopy')

        self.selectedPoint = None
        self.rect = None
        self.img_name = None

        self.ico = Image.open("image.ico")
        self.taskbar_process = None

        # pronalazenje rezolucije ekrana
        (self.width, self.height) = get_resolution()

        print(f"width = {self.width}, height = {self.height}")

        # drugi window
        self.select_window = Canvas(self.master, width=self.width, height=self.height, bg='red')

        #self.master.config(width=self.width, height=self.height)
        #self.select_window.config(width=200, height=200)

    def run(self):
        # podesavanje fullscreena
        self.master.attributes('-fullscreen', True)

        # podesavanje transparencije
        self.master.attributes('-alpha', 0.1)

        # bindujemo escape za izlazak
        self.master.bind('<Escape>', self.close)

        # events
        self.select_window.bind('<B1-Motion>', self.motion)  # da se binduje za motion ovaj frame
        self.select_window.bind('<Button>', self.first_click)
        self.select_window.bind('<ButtonRelease>', self.release)

        self.select_window.pack()

        #self.master.withdraw()

        menu=(item('Quit', self.close), item('Show', self.show_window))
        self.taskbar_process=pystray.Icon("name", self.ico, "title", menu)
        self.taskbar_process.run()

        self.master.mainloop()


    def show_window(self):
        self.taskbar_process.stop()
        self.master.after(0,self.master.deiconify())

    def close(self):
        #self.master.destroy()  # if you want to bring it back
        #self.taskbar_process.stop()
        #self.master.quit()

        self.master.withdraw()
        self.taskbar_process.run()




#EVENTI
    # funcija eventa za pracenje pomeranje misa
    def motion(self, event):
        print("Mouse position: (%s %s)" % (event.x, event.y))
        if self.selectedPoint is not None:
            self.select_window.coords(self.rect, self.selectedPoint[0], self.selectedPoint[1], event.x, event.y)
        return

    def first_click(self, event):
        #print("Mouse position: (%s %s)" % (event.x, event.y))
        self.selectedPoint = [event.x, event.y]
        self.rect = self.select_window.create_rectangle(self.selectedPoint[0],self.selectedPoint[1], self.selectedPoint[0], self.selectedPoint[1], fill="black")
        return

    def release(self, event):
        screen_shot_rectangle = [self.selectedPoint[0], self.selectedPoint[1], event.x, event.y]

        #print(f"{screen_shot_rectangle[0]} {screen_shot_rectangle[1]} {screen_shot_rectangle[2]} {screen_shot_rectangle[3]} ")

        (screen_shot_rectangle[0], screen_shot_rectangle[1], screen_shot_rectangle[2], screen_shot_rectangle[3]) =  \
        rearange_points(screen_shot_rectangle[0], screen_shot_rectangle[1], screen_shot_rectangle[2], screen_shot_rectangle[3])


        self.select_window.delete(self.rect)
        #self.image_name = self.take_screenshot([screen_shot_rectangle[0],screen_shot_rectangle[1]], [screen_shot_rectangle[2],screen_shot_rectangle[3]])
        self.image_name = take_screenshot2([screen_shot_rectangle[0],screen_shot_rectangle[1]], [screen_shot_rectangle[2],screen_shot_rectangle[3]])
        self.copy_text(self.image_name)
        self.selectedPoint = None
        self.rect = None
        return

    def take_screenshot(self, point1, point2):
        #print(point1, point2)
        image_name = "Screenshot.jpg"
        im = grab(bbox=(point1[0], point1[1], point2[0], point2[1]))
        im.save(image_name)
        return image_name


#Teseract ocr screen text translate
    def copy_text(self, image_name):
        tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        img = Image.open(image_name)
        text = tess.image_to_string(img)
        text = text[:-1]

        clipboard.copy(text[:-1])
        print(text)
        self.master.withdraw()
        del img


InstaCopy().run()
