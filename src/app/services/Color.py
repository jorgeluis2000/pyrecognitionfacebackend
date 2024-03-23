import numpy as np
from src.utils.function.ColorTransform import hsvToRgb, hsv_to_hex

class Color:
    
    def __init__(self, init_h: int, init_s: int, init_v: int) -> None:
        self.h = init_h
        self.s = init_s
        self.v = init_v
    
    def changeColorHSV(self, new_h: int, new_s: int, new_v: int):
        self.h = new_h
        self.s = new_s
        self.v = new_v
    
    def getColorHSV(self):
        return np.array([self.h, self.s, self.v])
    
    def getColorRGB(self):
        color_rgb = hsvToRgb([self.h, self.s, self.v])
        print(color_rgb)
        return color_rgb
    
    def getColorHex(self):
        return hsv_to_hex([self.h, self.s, self.v])