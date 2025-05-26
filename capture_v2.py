import mss
import mss.windows
import ctypes
from ctypes import wintypes
import time
import cv2
import numpy as np

usr = ctypes.windll.user32
usr.SetProcessDPIAware()
mss.windows.CAPTUREBLT = 0
mon = {'left': 0, 'top': 0, 'width': 1366, 'height': 768}

#

minimap_tl = cv2.imread('img/topleft.png', 0)
minimap_br = cv2.imread('img/bottomright.png', 0)

MMT_HEIGHT = max(minimap_tl.shape[0], minimap_br.shape[0])
MMT_WIDTH = max(minimap_tl.shape[1], minimap_br.shape[1])
#

char = cv2.imread('img/char.png', 0)
rune = cv2.imread('img/rune.png', 0)

char_height, char_width = char.shape


def test():
    hdl = usr.FindWindowW(None, 'Ranmelle')
    rect = ctypes.wintypes.RECT()
    usr.GetWindowRect(hdl, ctypes.pointer(rect))
    print("True")
    with mss.mss() as sct:
        output = "sct-{top}x{left}_{width}x{height}.png".format(**mon)

        sct_img = sct.grab(mon)

        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        print(output)


def screenshot(delay=1):
    hdl = usr.FindWindowW(None, 'Ranmelle')
    rect = ctypes.wintypes.RECT()
    usr.GetWindowRect(hdl, ctypes.pointer(rect))
    rect = (rect.left, rect.top, rect.right, rect.bottom)
    rect = tuple(max(0, x) for x in rect)
    mon['left'] = rect[0]
    mon['top'] = rect[1]
    mon['width'] = max(rect[2] - rect[0], MMT_WIDTH)
    mon['height'] = max(rect[3] - rect[1], MMT_HEIGHT)
    with mss.mss() as sct:
        try:
            return np.array(sct.grab(mon))
        except mss.exception.ScreenShotError:
            print('SS error')


# test()
screenshot()
