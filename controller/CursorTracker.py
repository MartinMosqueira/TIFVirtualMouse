import autopy
import threading

class CursorTracker:
    def __init__(self, smoothing, invert=False):
        # get screen size
        self.screen_width, self.screen_height = autopy.screen.size()

        self.prev_x = None
        self.prev_y = None
        self.smoothing = smoothing
        self.invert = invert

    def move_cursor(self, x, y):
        # off-screen detection
        if not (0 <= x <= 1 and 0 <= y <= 1):
            return

        # init position smoothing
        # this is to avoid the cursor jumping to a new position on the first frame
        if self.prev_x is None or self.prev_y is None:
            self.prev_x = x
            self.prev_y = y

        # new position smoothing
        smooth_x = self.prev_x * (1 - self.smoothing) + x * self.smoothing
        smooth_y = self.prev_y * (1 - self.smoothing) + y * self.smoothing

        if self.invert:
            smooth_x = 1 - smooth_x
            smooth_y = 1 - smooth_y

        # update preview position
        self.prev_x = smooth_x
        self.prev_y = smooth_y

        # calculate screen coordinates
        # autopy uses pixel coordinates, not percentage
        screen_x = self.screen_width * smooth_x
        screen_y = self.screen_height * smooth_y

        autopy.mouse.move(screen_x, screen_y)

    def click_cursor(self):
        threading.Thread(target=autopy.mouse.click).start()
        print("click cursor")
