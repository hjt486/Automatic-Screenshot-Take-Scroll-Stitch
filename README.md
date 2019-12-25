# Automatic-Screenshot-Take-Scroll-Stitch
### Introduction

There are a lot of websites that use server side rendering to only show part of the hi-res photo, in order to ask the users to pay for the photo, this is a program that automatically move mouse, do click, scroll action, and then take screenshots, and stitch them together to have the hi-res photo.



This is not a scripts that works universally, but you're allowed to modify as you want, there are two files:

`main.py`, this is a script used for website that has a small preview window, and when you click the low-res photo, it shows the hi-res part in the small preview window. The website I encountered used server side rendering, every time you click the low-res photo, it sends a request to the server side, and the server return a part of the hi-res photo to you, which is annoying because there is no way to get the full hi-res photo. I will spend a little more time later to comment and clean up the code, but since it can successfully done what I need, I won't spend too much time on make it "universal".  It simply receives two points (top left, and bottom right) to get the box of the photo, and run automatic click, get the screenshot of the preview window, go through entire low-res photo, and generated a merged hi-res photo.

`stitch.py ` this shares most same function as main.py, but, it works more like regular screenshot taker, however, when it takes the screenshot, it takes a window and then merge them together, so this is more like a practice for me before I finished the main.py.

### Required Modules

For Windows:
No need to install any modules.

For macOS (OS X):
sudo pip3 install pyobjc-framework-Quartz
sudo pip3 install pyobjc-core
sudo pip3 install pyobjc

For Linux:
sudo pip3 install python3-xlib
sudo apt-get install scrot
sudo apt-get install python3-tk
sudo apt-get install python3-dev

Then for all platforms:
sudo pip install pyautogui
sudo pip install pynput
sudo pip install pyscreenshot

Pauses and Fail-Safes:
Moving the mouse cursor to the upper-left
If unexpected problems happend
for On Windows and Linux:
Use CTRL-ALT-DEL to log out
for macOS (OS X):
SHIFT-OPTION-Q