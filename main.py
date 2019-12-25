import pyautogui
from pynput.mouse import Listener
from pynput import keyboard
import pyscreenshot as ImageGrab
from PIL import Image
import time

# Safety pause and turn on failsafe
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

class getPoint:
    def __init__(self):
        self.points = [0, 0]

    def get(self) -> bool:
        def on_move(x, y):
            #print ("Mouse moved")
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)

        def on_click(x, y, button, pressed):
            x, y = pyautogui.position()
            self.points = [x, y]
            return False

        def on_scroll(x, y, dx, dy):
            #print ("Mouse scrolled")
            pass

        try:
            listener = Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
            listener.start()
            while True:
                if not listener.isAlive():
                    break
            listener.stop()
            return self.points
        except KeyboardInterrupt:
            print('Get point failed.')
            return [0, 0]

class getScreenshot(object):
    def __init__(self, top_left, bottom_right, window_size, dpi_scale = 1):
        #self.top_left = [x * dpi_scale for x in top_left]
        #self.bottom_right = [x * dpi_scale for x in bottom_right]
        self.dpi_scale = dpi_scale
        #self.top_left = top_left
        self.top_left = [23, 69]
        self.bottom_right = bottom_right
        self.window_size = window_size
        print(top_left, bottom_right, window_size)
        self.horizontal_count = 0
        self.vertial_count = 0
        self.screenshots = []
        self.windows = []
        self.__calculateWindows()

    def __calculateWindows(self):
        top_left = self.top_left
        top_right = [self.bottom_right[0], self.top_left[1]]
        bottom_left = [self.top_left[0], self.bottom_right[1]]
        bottom_right = self.bottom_right
        print("Box coordinates: ",top_left, top_right, bottom_left, bottom_right)
        i = top_left[0]
        while i < top_right[0]:
            j = top_left[1]
            self.vertial_count = 0
            while j < bottom_right[1]:
                self.windows.append((i, j, i + self.window_size, j + self.window_size))
                self.vertial_count += 1
                j += self.window_size
            i += self.window_size
            self.horizontal_count += 1
        print(len(self.windows), self.horizontal_count, self.vertial_count)

    def __mergeScreenshots(self) -> Image:
        #x_offset = self.top_left[0] *  self.dpi_scale,
        #y_offset = self.top_left[1] *  self.dpi_scale,
        width = self.horizontal_count * self.window_size * self.dpi_scale
        height = self.vertial_count * self.window_size * self.dpi_scale
        merged_image = Image.new('RGB', (width, height))
        l = 0
        x = 0
        for i in range(self.horizontal_count):
            k = 0
            for j in range(self.vertial_count):
                merged_image.paste(im=self.screenshots[x], box=(l, k))
                k += self.window_size * self.dpi_scale
                x += 1
            l += self.window_size * self.dpi_scale
        return merged_image

    def get(self):
        screenshot_windows =(
            (self.top_left[0] + 528) * self.dpi_scale,
            (self.top_left[1] + 36) * self.dpi_scale,
            (self.top_left[0] + 530 + self.window_size) * self.dpi_scale, 
            (self.top_left[1] + 36 + self.window_size) * self.dpi_scale)
        for window in self.windows:
            pyautogui.moveTo(window[0], window[1], duration=0)
            pyautogui.click()
            time.sleep(1) 
            self.screenshots.append(ImageGrab.grab(bbox=screenshot_windows))
        img = self.__mergeScreenshots()
        img.show()
        img.save("result.png")
        """ for screentshot in self.screenshots:
            screentshot.show() """

class run:
    def __init__(self):
        self.top_left = [0,0]
        self.bottom_right = [0,0]
    
    def begin(self):
        def on_press(key):
            pass

        def on_release(key):
            if key == keyboard.Key.ctrl:
                point = getPoint()
                print("Click the top left corner to get coordinates.")
                self.top_left = point.get()
                print("Click the bottom right corner to get coordinates.")
                time.sleep(0.5) 
                self.bottom_right = point.get()
                print("Top left and bottom right: ", self.top_left, self.bottom_right)
                return False
        try:
            listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            listener.start()
            while True:
                if not listener.isAlive():
                    break
            listener.stop()
            return self.top_left, self.bottom_right

        except KeyboardInterrupt:
            print('Get point failed.')
            return False
        
def main():
    print('Press Ctrl + C to quit.')
    dpi_scale = int(input("Enter your screen scale (Mac Retina is 2): "))
    try:
        print('Press Ctrl to start.')
        program = run()
        top_left, bottom_right = program.begin()
        screenshot = getScreenshot(top_left, bottom_right, 114, dpi_scale)
        screenshot.get()

    except KeyboardInterrupt:
        print('Exit')

if __name__ == "__main__":
    main()