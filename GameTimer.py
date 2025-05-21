from graphics import *

class GameTimer():
    def __init__(self, win):
        self.beforeTime = 0
        self.minute = 0
        self.second = 0
        self.timer = Text(Point(400, 550), f"{str(self.minute).zfill(2)}:{str(self.second).zfill(2)}")
        self.timer.setSize(20)
        self.timer.draw(win)

    # def main(self, worldTime, win):

    #     if(worldTime - self.beforeTime >= 60):
    #         self.beforeTime = worldTime
    #         self.second += 1
    #         if(self.second == 60):
    #             self.minute += 1
    #             self.second = 0
            
    #         self.timer.setText(f"{str(self.minute).zfill(2)}:{str(self.second).zfill(2)}")
        
    #     self.redrawTimer(win)
    def main(self, worldTime, win):

        self.minute = int(worldTime/3600)
        self.second = int(worldTime%3600/60)
            
        self.timer.setText(f"{str(self.minute).zfill(2)}:{str(self.second).zfill(2)}")
        
        self.redrawTimer(win)
    
    def undrawTimer(self):
        self.timer.undraw()

    def redrawTimer(self, win):
        self.timer.undraw()
        self.timer.draw(win)
    
    def getTime(self):
        return f"{str(self.minute).zfill(2)}:{str(self.second).zfill(2)}"