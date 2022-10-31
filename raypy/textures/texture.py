from abc import abstractmethod


class Texture:
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_color(self, hit):
        pass


class SolidColor(Texture):
    def __init__(self, color):
        self.color = color

    def get_color(self, hit):
        return self.color
