import math

def dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def distObj(obj1, obj2):
    return dist(obj1.getX(), obj1.getY(), obj2.getX(), obj2.getY())

