import pyautogui
from pynput.mouse import Listener
from pynput import keyboard
import pyscreenshot as ImageGrab
from PIL import Image
import time

# Safety pause and turn on failsafe
pyautogui.PAUSE = 1.5
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
        self.top_left = [x * dpi_scale for x in top_left]
        self.bottom_right = [x * dpi_scale for x in bottom_right]
        self.window_size = window_size * dpi_scale
        print(top_left, bottom_right, window_size)
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
            while j < bottom_right[1]:
                self.windows.append((i, j, i + self.window_size, j + self.window_size))
                j += self.window_size
            i += self.window_size
        print(len(self.windows))

    def __mergeScreenshots(self) -> Image:
        x_offset = self.top_left[0]
        y_offset = self.top_left[1]
        width = self.bottom_right[0] - self.top_left[0]
        height = self.bottom_right[1] - self.top_left[1]
        merged_image = Image.new('RGB', (width, height))
        for i, screenshot in enumerate(self.screenshots):
            merged_image.paste(im=screenshot, box=(self.windows[i][0]-x_offset, self.windows[i][1]-y_offset))
        return merged_image

    def get(self):
        for window in self.windows:
            self.screenshots.append(ImageGrab.grab(bbox=window))
        self.__mergeScreenshots().show()
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
                time.sleep(1) 
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
        screenshot = getScreenshot(top_left, bottom_right, 188, dpi_scale)
        screenshot.get()

    except KeyboardInterrupt:
        print('Exit')

if __name__ == "__main__":
    main()