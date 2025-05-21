from graphics import *
class Character(Image):
    def __init__(self, x, y, hp, maxhp, speed, *pixmap):
        super().__init__(Point(x,y),pixmap)

        # 初期座標
        self.x = x
        self.y = y
        # 体力
        self.hp = hp
        # 体力の最大値
        self.maxhp = maxhp
        # 速度
        self.speed = speed
        # キャラクターの死亡判定
        self.dead = False

    def move(self, dx, dy):
        super().move(dx,dy)

    def isDead(self):   #追加
        """死亡していたらself.deadをTrueにする"""  
        if self.hp<=0:
            self.dead=True
        return self.dead
    
    def isHit(self,target,range):   #追加
        """自分からx,y軸ともに±rangeにtargetがいたらTrueいないとFalse"""
        if (self.x-range < target.x < self.x+range) and (self.y-range<target.y<self.y+range):
            return True
        else:
            return False