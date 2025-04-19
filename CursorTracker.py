import autopy

class CursorTracker:
    def __init__(self):
        #Get screen size
        self.screen_width, self.screen_height = autopy.screen.size()

    def move_cursor(self, x, y):
        if 0 <= x <= 1 and 0 <= y <= 1:
            autopy.mouse.move(self.screen_width * x, self.screen_height * y)
