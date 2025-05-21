class WorldTime():
    def __init__(self):
        self.time=0

    def advanceTime(self):
        self.time += 1

    def getTime(self):
        return self.time
    
    def advanceTime1(self):
        self.time += 3600