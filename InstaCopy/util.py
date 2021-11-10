import ctypes

import win32gui
import win32ui
import win32con

def get_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def take_screenshot2(point1, point2):
    try:
        bmpfilenamename = "out.bmp" #set this

        hwnd = win32gui.FindWindow(None, "master")

        wDC = win32gui.GetWindowDC(hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, point2[0] - point1[0], point2[1] - point1[1])
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (point2[0] - point1[0], point2[1] - point1[1]), dcObj, (point1[0], point1[1]), win32con.SRCCOPY)
        dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)

        # Free Resources
        win32gui.DeleteObject(dataBitMap.GetHandle())
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)

        return bmpfilenamename

        #win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)



    except Exception as e:
        print(e)


def rearange_points(x1, y1 , x2, y2):
    if x1 > x2:
        temp = x1
        x1 = x2
        x2 = temp

    elif x1 == x2:
        x2 += 1

    if y1 > y2:
        temp = y1
        y1 = y2
        y2 = temp

    elif y1 == y2:
        y2 += 1

    return x1, y1, x2, y2