import autopy
import pyautogui

class CursorTracker:
    def __init__(self):
        #Obtener tamanio de pantalla
        self.screen_width, self.screen_height = autopy.screen.size()

    def move_cursor(self, x, y):
        autopy.mouse.move(self.screen_width * x, self.screen_height * y)
