from PIL import Image
import pyautogui
import pyscreenshot as ImageGrab

frame_location = pyautogui.locateOnScreen("frame.png", grayscale=True, confidence=.98)
frame = Image.open("frame.png")
internal_frame = Image.open("internal_frame.png")
width_height =  internal_frame.size[0]
offset = frame.size[0] - width_height
top_left, bottom_right = frame_location[0], frame_location[1]
im = ImageGrab.grab(bbox=(top_left + offset/2, bottom_right + offset/2, top_left + offset/2 + width_height, bottom_right + offset/2 + width_height))
im.show()
im.save("test.png")
print(top_left, bottom_right, width_height)