import capture
import numpy as np


PLAYER_BGRA = (68, 221, 255, 255)
RUNE_BGRA = (255, 102, 221, 255)
ENEMY_BGRA = (0, 0, 255, 255)
GUILD_BGRA = (255, 102, 102, 255)
BUDDY_BGRA = (225, 221, 17, 255)


class Game:
    def __init__(self, region):
        self.hwnd = capture.find_window_from_executable_name("MapleStory.exe") #process
        self.top, self.left, self.bottom, self.right = region[0], region[1], region[2], region[3]

    def get_rune_image(self):
        with capture.CaptureWindow(self.hwnd) as img:
            if img is None:
                print("Process was not found.")
                return None
            return img.copy()

    def locate(self, *color):
        with capture.CaptureWindow(self.hwnd) as img:
            locations = []
            if img is None:
                print("MapleStory.exe was not found.")
            else:
                img_cropped = img[self.left:self.right, self.top:self.bottom]
                height, width = img_cropped.shape[0], img_cropped.shape[1]
                img_reshaped = np.reshape(img_cropped, ((width * height), 4), order="C")
                for c in color:
                    sum_x, sum_y, count = 0, 0, 0
                    matches = np.where(np.all((img_reshaped == c), axis=1))[0]
                    for idx in matches:
                        sum_x += idx % width
                        sum_y += idx // width
                        count += 1
                    if count > 0:
                        x_pos = sum_x / count
                        y_pos = sum_y / count
                        locations.append((x_pos, y_pos))
            return locations

    def get_player_location(self):
        location = self.locate(PLAYER_BGRA)
        return location[0] if len(location) > 0 else None

    def get_rune_location(self):
        location = self.locate(RUNE_BGRA)
        return location[0] if len(location) > 0 else None
