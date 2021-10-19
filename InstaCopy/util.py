import ctypes

def get_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]