import cv2 as cv
import win32gui, win32ui, win32con, win32api
import random
import time

# general program flow:
# 1. arguments are location of the bookmark, window itself
#     and image of the buy button i guess
# 2. create its predicted y value by getting 3/4ths of the y pos
#     (consider looking at how the crosshair was made in visions)
# 3. matchtemplate for the buy button
# 4. click the button in a random position
# 5. match template the next buy button
# 6. quickly after click the buy button

class Buy:
    a = 20
    t = 600
    hwnd = None

    def __init__(self, hwnd) :
        self.hwnd = hwnd

    def buy(self,top_crop, y ,h, debug_mode=True) : ## change later:
        # get hwnd location, then click on the point within the hwnd
        #or click directly within the hwnd

        rect = win32gui.GetWindowRect(self.hwnd)
        rand = round(self.rand())
        rt = self.randtime()

        window_x = rect[0]
        window_y = rect[1]
        window_width = rect[2] - rect[0]
        window_height = rect[3] - rect[1]

        # ROI_x is based off of the buy button position, not off of the original x location
        ROI_x = int( window_x +  (window_width * 8/9) + 2 * rand)
        ROI_y = int( h * 7/9 ) + top_crop + y + int(rand/2)

        buy_x = round (window_x + 3/5 * window_width) - rand
        buy_y = round (window_y + 5/7 * window_height) + rand

        time.sleep(0.2)

        self.click(ROI_x,ROI_y)
        time.sleep(0.3 + rt)
        # location based purchasing 
        self.click(buy_x , buy_y)
        time.sleep(0.3 + rt)


    def click(self, x, y) :
        win32api.SetCursorPos( (x, y) )
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0 , 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0 , 0)

    def scroll(self) :
        rand = round(self.rand())
        rt = self.randtime()
        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0] + 3 * rand
        y = rect[1] + 2 * rand
        w = rect[2] - x
        h = rect[3] - y
        win32api.SetCursorPos( (round(x + 3/4 * w), round(y + 3/4 *h)) )
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0 , 0)
        time.sleep(0.2 + rt)
        win32api.SetCursorPos( (round(x + 3/4 * w), round(y + 1/3 *h)) )
        time.sleep(0.1 + rt)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0 , 0)
        time.sleep(0.9 + rt/3)

    def refresh(self) :
        rand = round(self.rand())
        rt = self.randtime()        
        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0] + 7 * rand
        y = rect[1] + 2 * rand
        w = rect[2] - x
        h = rect[3] - y
        self.click(round(x + 2/9 * w) , round(y + 8/9 *h))
        time.sleep(0.4 + rt)
        self.click(round(x + 4/7 * w) , round(y + 5/8 *h))

    def randtime(self) :
        return random.randint(0,self.t) / 1000
    
    def rand(self) :
        return random.randint(0,self.a) - self.a/2