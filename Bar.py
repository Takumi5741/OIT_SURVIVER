from graphics import *
class Bar():
    def __init__(self,x,y,height,maxwidth,value,maxvalue):
        self.x = x
        self.y = y
        self.height = height
        self.maxwidth = maxwidth
        self.baseBar = Rectangle(Point(x-1, y-1), Point(x+maxwidth+1, y+height+1))
        self.bar = Rectangle(Point(x, y),Point(x+maxwidth*value/maxvalue, y+height))
        self.baseBar.setFill("black")
        self.baseBar.setOutline("black")

    def createBar(self,win):
        self.baseBar.draw(win)
        self.bar.draw(win)

    def delateBar(self):
        self.baseBar.undraw()
        self.bar.undraw()

class HpBar(Bar):
    def __init__(self,target,color):
        x = target.x - target.range
        y = target.y + target.range
        height = 2
        maxwidth = target.range * 2
        value = target.hp
        maxvalue = target.maxhp
        super().__init__(x, y, height, maxwidth, value, maxvalue)
        self.bar.setFill(color)
        self.bar.setOutline(color)
        

class ExperienceBar(Bar):
    def __init__(self,x,y,maxwidth,player):
        height = 6
        value = player.experience
        maxvalue = player.maxexperience
        super().__init__(x, y, height, maxwidth, value, maxvalue)
        self.bar.setFill("cyan")
        self.bar.setOutline("cyan")

        self.label = Text(Point(x+maxwidth-50,550),'Levels:'+str(player.level))
        self.label.setSize(16)
        self.label.setTextColor('black')

    def createBar(self,win):
        self.label.draw(win)
        super().createBar(win)

    def changeBar(self,player,win):
        self.bar.undraw()
        self.label.undraw()
        value = player.experience
        maxvalue = player.maxexperience

        self.bar = Rectangle(Point(self.x, self.y),Point(self.x+self.maxwidth*value/maxvalue, self.y+self.height))
        self.bar.setFill("cyan")
        self.bar.setOutline("cyan")
        self.bar.draw(win)

        self.label.setText('Levels:'+str(player.level))
        self.label.draw(win)

    def delateBar(self):
        self.label.undraw()
        super().delateBar()
