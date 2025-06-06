import time
import math
import autopy
import pyautogui
import threading

class AdaptiveCursor:
    def __init__(self, alpha_min, alpha_max, speed_sens):
        self.alpha_min = alpha_min
        self.alpha_max = alpha_max
        self.speed_sens = speed_sens
        # get screen size
        self.screen_w, self.screen_h = autopy.screen.size()

        self.prev_x = self.prev_y = None
        self.prev_t = None
        self.prev_sx = self.prev_sy = None

    def move(self, x, y):
        # off-screen detection
        if not (0 <= x <= 1 and 0 <= y <= 1):
            return

        now = time.time()
        if self.prev_x is None or self.prev_y is None:
            # init position
            self.prev_x, self.prev_y = x, y
            self.prev_t = now
            self.prev_sx, self.prev_sy = x, y
            autopy.mouse.move(int(x*self.screen_w), int(y*self.screen_h))
            return

        # calculate the exact frame rate
        dt = now - self.prev_t
        dx, dy = x - self.prev_x, y - self.prev_y
        dist = math.hypot(dx, dy)
        speed = dist / dt if dt > 0 else 0

        # adjusts smoothed based on frame rate
        frac = speed / (speed + self.speed_sens)

        # interpolates the value between min and max
        alpha = self.alpha_min + (self.alpha_max - self.alpha_min) * frac

        # EMA filter
        sx = alpha * x + (1 - alpha) * self.prev_sx
        sy = alpha * y + (1 - alpha) * self.prev_sy

        # move cursor
        screen_x = int(sx * self.screen_w)
        screen_y = int(sy * self.screen_h)
        autopy.mouse.move(screen_x, screen_y)

        # update values
        self.prev_x, self.prev_y = x, y
        self.prev_sx, self.prev_sy = sx, sy
        self.prev_t = now

    def click_left_cursor(self):
        threading.Thread(target=autopy.mouse.click).start()

    def click_right_cursor(self):
        threading.Thread(target=autopy.mouse.click, args=(autopy.mouse.Button.RIGHT,)).start()

    def scroll_down_cursor(self):
        threading.Thread(target=pyautogui.scroll, args=(pyautogui.scroll(-5))).start()

    def scroll_up_cursor(self):
        threading.Thread(target=pyautogui.scroll, args=(pyautogui.scroll(5))).start()