import pyautogui
from pynput.mouse import Listener
from pynput import keyboard
import pyscreenshot as ImageGrab
from PIL import Image
import time

'''
Safety pause and turn on failsafe
Go check pyautogui document for details
'''
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

'''
This is a class to get the coordinates on screen by monitoring mouse clicking
'''
class getPoint:
    @staticmethod
    def get() -> bool:
        point = [0, 0]
        def on_move(x, y):
            #print ("Mouse moved")
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)

        def on_click(x, y, button, pressed):
            #print ("Mouse clicked")
            point[0], point[1] = pyautogui.position()
            return False

        def on_scroll(x, y, dx, dy):
            #print ("Mouse scrolled")
            pass

        try:
            # Start the listener for mouse clicking
            listener = Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
            listener.start()
            while True:
                if not listener.isAlive():
                    break
            listener.stop()
            return point
        except KeyboardInterrupt:
            print('Get point failed!')
            return point

'''
This is the class to perform screenshot taking and merging
'''
class getScreenshot(object):
    def __init__(self, top_left, bottom_right, window_size, frame_size, frame_topleft, dpi_scale = 1, delay = 1):
        # All coordinates and window size variables
        self.dpi_scale = dpi_scale
        self.top_left = top_left
        self.bottom_right = bottom_right
        if window_size < frame_size:
            self.window_size = window_size
        else:
            self.window_size = frame_size
        self.frame_size = frame_size
        self.frame_topleft = frame_topleft

        # Count how many windows needed horizontally and vertically
        self.horizontal_count = 0
        self.vertical_count = 0

        # Two empty array for holding windows coordinates and screenshots
        self.screenshots = []
        self.windows = []
        
        # Control the delay
        self.delay = delay

        # Run internal method to calcualte all windows for screenshots
        self.__calculateWindows()

    # Pre-calcualte all windows for screenshots
    def __calculateWindows(self):
        top_left = self.top_left
        top_right = [self.bottom_right[0], self.top_left[1]]
        bottom_left = [self.top_left[0], self.bottom_right[1]]
        bottom_right = self.bottom_right
        print("Box coordinates: ",top_left, top_right, bottom_left, bottom_right)
        i = top_left[0]
        while i < top_right[0]:
            j = top_left[1]
            self.vertical_count = 0
            while j < bottom_right[1]:
                self.windows.append((i, j, i + self.window_size, j + self.window_size))
                self.vertical_count += 1
                j += self.window_size
            i += self.window_size
            self.horizontal_count += 1
        print("Total ", str(len(self.windows)), " screenshots to be take.")
        print("Horizontally: ", self.horizontal_count, ", vertically: ", self.vertical_count, ".")

    # Merge all screenshots into one single image
    def __mergeScreenshots(self) -> Image:
        print("Begin merging all screenshots...")
        width = self.horizontal_count * self.window_size * self.dpi_scale
        height = self.vertical_count * self.window_size * self.dpi_scale
        merged_image = Image.new('RGB', (width, height))
        l = 0
        x = 0
        for i in range(self.horizontal_count):
            k = 0
            for j in range(self.vertical_count):
                merged_image.paste(im=self.screenshots[x], box=(l, k))
                k += self.window_size * self.dpi_scale
                x += 1
            l += self.window_size * self.dpi_scale
        return merged_image

    # Main method to start get screenshots
    def get(self):
        # This is where the frame is located
        screenshot_window =(
            self.frame_topleft[0] * self.dpi_scale,
            self.frame_topleft[1] * self.dpi_scale,
            (self.frame_topleft[0] + self.frame_size) * self.dpi_scale,
            (self.frame_topleft[1] + self.frame_size) * self.dpi_scale)
        print("Begin taking screenshots...")
        # Move mouse one window by one window and take the screenshotså
        for window in self.windows:
            pyautogui.moveTo(window[0], window[1], duration=0)
            pyautogui.click()
            time.sleep(self.delay) 
            self.screenshots.append(ImageGrab.grab(bbox=screenshot_window))
        # Merge the screenshots and return the image
        img = self.__mergeScreenshots()
        # Preview the image
        img.show()
        # Save the image on disk
        filename = "result.png"
        img.save(filename)
        print("Merged result has been saved to " + filename + " .")
        """ for screentshot in self.screenshots:
            screentshot.show() """

'''
This is the class to detect the frame, you need to pre-define the frame images
On the disk as 'frame.png' and 'internal_frame.png'
'''
class getFrameLocation(object):
    @staticmethod
    def get(confidence_factor = 0.98, dpi_scale = 1):
        # Find the frame on the screen.
        frame_location = pyautogui.locateOnScreen("frame.png", grayscale=True, confidence= confidence_factor)
        if frame_location:
            frame = Image.open("frame.png")
            internal_frame = Image.open("internal_frame.png")
            # Calculate the offset of internal and external frame
            width_height =  internal_frame.size[0]
            offset = (frame.size[0] - width_height)/2
            x, y = frame_location[0] + offset, frame_location[1] + offset
            """
            # test purpose to show the internal frame
            # to check if it is on correct position
            im = ImageGrab.grab(bbox=(
                x, y,
                x + width_height,
                y + width_height))
            im.show()  
            """
            return x/dpi_scale, y/dpi_scale, width_height/dpi_scale, offset
        else:
            return False

'''
A class wait for Ctrl key to start selecting point
'''
class wait(object):
    @staticmethod
    def forKey(delay):
        top_left = [0, 0]
        bottom_right = [0, 0]

        def on_press(key):
            pass

        def on_release(key):
            if key == keyboard.Key.ctrl:
                print("Click the top left corner to get coordinates.")
                top_left[0], top_left[1] = getPoint.get()
                print("Click the bottom right corner to get coordinates.")
                time.sleep(delay) 
                bottom_right[0], bottom_right[1] = getPoint.get()
                print("Top left and bottom right: ", top_left, bottom_right)
                return False

        try:
            listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            listener.start()
            while True:
                if not listener.isAlive():
                    break
            listener.stop()
            return top_left, bottom_right

        except KeyboardInterrupt:
            print('Get point failed!')
            return False
        
def main():
    '''
    Customize the parameters here,
    Please firstly change the frame images in the folder,
    Therefore the program can detect the frame, if you see border on the result
    Try decrese the internal frame size few pixels to avoid borders, this may happen on 
    DPI scalling enabled monitor, such as Apple Retina display beacaue of the scalling
    '''
    dpi_scale = 2 # Mac retina is 2, 
    '''
    Scan window size, should be smaller than frame size
    Smaller window size will have better result to prevent stitching effect
    Theoretically you can make it as small as 1px
    But it can be very slow, so try several time for best balance.
    '''
    scan_window_size = 50
    '''
    This is the delay for each screenshot taking (the interval to move the cursor)
    The problem is that you have to wait until the server to return the rendered result
    If the delay is too small, the result may not be return to the preview window
    Depends on the server reaction time and your internet condition, choose wisely
    '''
    delay = 1
    '''
    This is for frame detection, the program will look for the frame you defined on disk
    in 'frame.png' and 'internal_frame.png', the most important one is 'frame.png',
    The program will look for an area on screen that is similair to 'frame.png',
    the condidence factor is a threshold of how similiar it decides to be the same frame
    If it is to small, the detection may have little offs
    But if it is 1, it's usually impossible due to the screen color/rendering difference
    'internal_frame.png' only used for getting size of internal frame, the content and image
    itself is irrelevant.

    DON'T CHANGE IT UNLESS YOU CANNOT FIND THE FRAME YOU DEFINED!!!!
    '''
    confidence_factor = 0.98

    print('Press Ctrl + C to quit.')
    try:
        ifGetFrameLocation = False
        while not ifGetFrameLocation:
            message = " Please open the webpage for frame detection..."
            print(message, end='')
            print('\b' * len(message), end='', flush=True)
            ifGetFrameLocation = getFrameLocation.get(confidence_factor, dpi_scale)
        print("\nFrame detected!", ifGetFrameLocation)
        frame_topleft = (int(ifGetFrameLocation[0]), int(ifGetFrameLocation[1]))
        frame_window = int(ifGetFrameLocation[2])
        print('Press Ctrl to start.')
        top_left, bottom_right = wait.forKey(0.5)
        screenshot = getScreenshot(top_left, bottom_right, scan_window_size, frame_window, frame_topleft, dpi_scale, delay)
        screenshot.get()

    except KeyboardInterrupt:
        print('Exit')

if __name__ == "__main__":
    main()