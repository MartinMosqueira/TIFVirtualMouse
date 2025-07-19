from abc import ABC, abstractmethod


class CursorInterface(ABC):

    @abstractmethod
    def move(self, x, y):
        pass

    @abstractmethod
    def click_left_cursor(self):
        pass

    @abstractmethod
    def click_right_cursor(self):
        pass

    @abstractmethod
    def scroll_down_cursor(self):
        pass

    @abstractmethod
    def scroll_up_cursor(self):
        pass
