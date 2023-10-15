import cv2 as cv
import os
from windowcapture import WindowCapture
from vision import Vision
from buy import Buy
import win32gui
import keyboard
import random
# delete after
import time
import BM_CONSTANTS as const

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Debug State
debug = False


#initialize the hwnd and titlebar as a basic parameter
top_crop = const.top_crop
hwnd = None
if const.window_path is None: 
      print('Exception: No Valid Window Detected. Program Terminating')
else:
    hwnd = win32gui.FindWindow(None, const.window_path)
    if not hwnd:
        raise Exception('Window not found: {}'.format(const.window_path))


rect = win32gui.GetWindowRect(hwnd)
half_crop = round( (rect[3] - rect[1] ) / 2)


# initialize the WindowCapture class
wincap = WindowCapture(hwnd, top_crop)
# initialize an array of paths for the vision class

# initialize the Vision class for all visions
vision_BM = Vision(const.needle_paths)

buyer = Buy(hwnd)

def MatchBuy(cropped=False) :
       # get an updated image of the game
    screenshot = wincap.get_screenshot()
    if(cropped) :
        screenshot = screenshot[half_crop:rect[3], 0:rect[2]]
        points = vision_BM.find_all(screenshot, 0.95)

        for (x,y,w,h) in points:
            location = buyer.buy(top_crop ,y + half_crop,h, debug_mode=debug)
    else :
    # display the processed image
        points = vision_BM.find_all(screenshot, 0.95)
        if(debug) : print(points)
        for (x,y,w,h) in points:
            buyer.buy(top_crop,y ,h, debug_mode=debug)

    if (debug) :
        cv.imshow('Matches', screenshot) 
    

# Do the process twice, once swiping downwards
while(True):
    MatchBuy(False)
    buyer.scroll()
    MatchBuy(True)
    buyer.refresh()
    
    # add a termination clause when out of gold

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(2000) == ord('q'):
        cv.destroyAllWindows()
        break


    if keyboard.is_pressed('ctrl') :  # if key 'q' is pressed 
        print('Terminating program')
        break
    

print('Done.')