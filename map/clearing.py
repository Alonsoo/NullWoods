import math
import util

class ClearingCircle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
    
    def maxRadiusForCircleAt(self, x, y):
        d = util.dist(self.x, self.y, x, y)
        return max(-1, d - self.r)
    
    def drawBounds(self):
        pass

    def setPos(self, x, y):
        self.x = x
        self.y = y


    
class ClearingRect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def maxRadiusForCircleAt(self, x, y):
        d1 = self.x - x
        d2 = x - (self.x + self.w)
        d3 = self.y - y
        d4 = y - (self.y + self.h)
        return max(-1, d1, d2, d3, d4)
    
    def drawBounds(self):
        pass
