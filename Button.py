from graphics import *

class Button():
    def __init__(self, center, width, height, label):
        w, h = width / 2.0, height / 2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.label = Text(center, label)
        self.active = False
    
    def isclicked(self, p):
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def drawButton(self, win):
        self.rect.draw(win)
        self.label.draw(win)
        self.active = True
    
    def undrawButton(self):
        self.rect.undraw()
        self.label.undraw()
        self.active = False