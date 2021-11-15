from infi.systray import SysTrayIcon

class sysTray:

    def __init__(self):
        menu_options = (("Take screenshot", None, self.take_screenshot),)
        self.taskbar_process = SysTrayIcon("Data\image.ico", "InstantCopy", menu_options, on_quit=self.kill_icon_tray)
        self.taskbar_process.start()

    def take_screenshot(self, event):
        print("take screenshot")

    def kill_icon_tray(self, event):
        self.taskbar_process.shutdown()

s = sysTray()