from tkinter import *
from util import *

import sys

import pytesseract as tess
from PIL import Image

import clipboard

import win32gui
import win32ui
import win32api
import win32con
import win32process

import pystray

from pynput.keyboard import Listener
from threading import Thread
import multiprocessing

from infi.systray import SysTrayIcon

ctypes.windll.shcore.SetProcessDpiAwareness(2)



class InstantCopy:
    def __init__(self):

        self.closing = False

        self.ico = Image.open("Data\image.ico")
        self.menu = None
        self.taskbar_process = None

        self.shortcut_key = "'p'"  # str("'\\x10'")
        self.thread_status = True

        #self.shortcut_thread = Thread(target=self.thread_function)
        #self.shortcut_thread = multiprocessing.Process(target=self.thread_function)
        #self.shortcut_thread.start()

        self.key_listener = Listener(on_press=self.on_press)
        self.key_listener.start()

        menu_options = (("Take screenshot", None, self.take_screenshot),)
        self.taskbar_process = SysTrayIcon("Data\image.ico", "InstantCopy", menu_options, on_quit=self.kill_icon_tray)
        self.taskbar_process.start()

        self.gui = Gui()
        self.gui.run()
        #self.gui.master.destroy()


        #self.taskbar_process.shutdown()

        self.key_listener.stop()
        #self.key_listener.join()


        #self.taskbar_process.start()
        #self.taskbar_process.shutdown()

        t, p = win32process.GetWindowThreadProcessId(self.taskbar_process.hwnd)
        win32gui.PostMessage(self.taskbar_process.hwnd, win32con.WM_CLOSE,0,0)
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p)
            if handle:
                win32api.TerminateProcess(handle,0)
            win32api.CloseHandle(handle)
        except:
            print("Exception")


    def on_press(self, key):
        if not self.closing:
            print(str(key))
            if str(key) == "Key.esc":
                self.gui.hide("nothing")
            if str(key) == self.shortcut_key:
                self.gui.show_window()
        else:
            print("return")

    def thread_function(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()


    def kill_icon_tray(self, event):

        self.closing = True
        print("Close the whole application")
        #self.taskbar_process.shutdown()
        self.gui.master.destroy()


    def take_screenshot(self, event):
        self.gui.show_window()


class Gui():
    def __init__(self):
        self.master = Tk(className='InstantCopy')

        self.selectedPoint = None
        self.rect = None
        self.img_name = "Screenshot.bmp"

        # self.shortcut_key = "'p'" #str("'\\x10'")

        # pronalazenje rezolucije ekrana
        (self.width, self.height) = get_resolution()

        # print(f"width = {self.width}, height = {self.height}")

        # drugi window
        self.select_window = Canvas(self.master, width=self.width, height=self.height, bg='red')

        # self.master.config(width=self.width, height=self.height)
        # self.select_window.config(width=200, height=200)

    def run(self):
        # podesavanje fullscreena
        self.master.attributes('-fullscreen', True)

        # podesavanje transparencije
        self.master.attributes('-alpha', 0.1)

        # bindujemo escape za izlazak
        self.master.bind('<Escape>', self.hide)
        self.master.bind('p', self.show_window())

        # events
        self.select_window.bind('<B1-Motion>', self.motion)  # da se binduje za motion ovaj frame
        self.select_window.bind('<Button>', self.first_click)
        self.select_window.bind('<ButtonRelease>', self.release)

        self.select_window.pack()

        self.master.withdraw()
        self.master.mainloop()

    def show_window(self):
        self.master.after(0, self.master.deiconify())

    def hide(self, event):
        self.master.withdraw()

    def close(self, event):
        print("GI close")
        #self.master.quit()
        #self.select_window.destroy()
        self.master.destroy()
        #self.master.quit()
        return

    # EVENTI
    # funcija eventa za pracenje pomeranje misa
    def motion(self, event):
        # print("Mouse position: (%s %s)" % (event.x, event.y))
        if self.selectedPoint is not None:
            self.select_window.coords(self.rect, self.selectedPoint[0], self.selectedPoint[1], event.x, event.y)
        return

    def first_click(self, event):
        # print("Mouse position: (%s %s)" % (event.x, event.y))
        self.selectedPoint = [event.x, event.y]
        self.rect = self.select_window.create_rectangle(self.selectedPoint[0], self.selectedPoint[1],
                                                        self.selectedPoint[0], self.selectedPoint[1], fill="black")
        return

    def release(self, event):
        screen_shot_rectangle = [self.selectedPoint[0], self.selectedPoint[1], event.x, event.y]

        # print(f"{screen_shot_rectangle[0]} {screen_shot_rectangle[1]} {screen_shot_rectangle[2]} {screen_shot_rectangle[3]} ")

        (screen_shot_rectangle[0], screen_shot_rectangle[1], screen_shot_rectangle[2], screen_shot_rectangle[3]) = \
            rearange_points(screen_shot_rectangle[0], screen_shot_rectangle[1], screen_shot_rectangle[2],
                            screen_shot_rectangle[3])

        self.select_window.delete(self.rect)
        # self.image_name = self.take_screenshot([screen_shot_rectangle[0],screen_shot_rectangle[1]], [screen_shot_rectangle[2],screen_shot_rectangle[3]])
        take_screenshot(self.img_name, [screen_shot_rectangle[0], screen_shot_rectangle[1]],
                        [screen_shot_rectangle[2], screen_shot_rectangle[3]])
        self.copy_text(self.img_name)
        self.selectedPoint = None
        self.rect = None
        return

    # Teseract ocr screen text translate
    def copy_text(self, image_name):
        tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        img = Image.open(image_name)
        text = tess.image_to_string(img)
        text = text[:-1]

        clipboard.copy(text[:-1])
        print(text)
        self.hide("nothing")
        del img


if __name__ == '__main__':
    InstantCopy()
    # InstaCopy().run()
