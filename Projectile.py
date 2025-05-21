from graphics import *
from Character import *
from WorldTime import *
import math

# 飛び道具のクラス　キャラクターを継承しているが、こちらのほうが管理しやすい
class Projectile(Character):
    def __init__(self, x, y, *pixmap):
        super().__init__(x, y, 0, 0, 0, *pixmap) # ここの0,0はCharacterクラスの都合上無視してよい
        self.range = 16    #当たり判定の広さ
        self.fUse = True #利用可能かどうかを示す。Trueなら可能

    def move(self, X, Y, s, speed):
        dx = X/s*speed
        dy = Y/s*speed
        self.x = self.x+dx
        self.y = self.y+dy
        super().move(dx,dy)

    def hit(self,target,damage):
        """第一引数にターゲットのmonster,第二引数にProjectileのdamage"""

        if super().isHit(target,self.range):
            target.hp -= damage            
            self.damage = 0
            self.fUse = False

    def canUse(self):
        if not(0 <= self.x < 800 and 0 <= self.y < 600):
            return False
        return self.fUse
    
class magicFire(Projectile):
    def __init__(self, myX, myY, targetX, targetY, msRate, maRate):
        super().__init__(myX, myY, "./img/magicFire2.png")
        self.speed = 4.0 * msRate   #飛翔速度
        self.damage = 5 * maRate    #与えるダメージ
        self.X = targetX-self.x
        self.Y = targetY-self.y
        self.s = math.sqrt(self.X*self.X+self.Y*self.Y)

    def move(self):
        return super().move(self.X, self.Y, self.s, self.speed)
    
    def hit(self, target):
        return super().hit(target, self.damage)
    
class Eye(Projectile):
    def __init__(self, myX, myY, targetX, targetY, nowtime):
        super().__init__(myX, myY, "./img/eye2.png")
        self.speed = 0.15        #最初の飛翔速度
        self.changeSpeed = 5  #変化後の飛翔速度
        self.damage = 10         #与えるダメージ
        self.coolTimeC = 1      #生成後に速度が変化する時間
        self.spawnTime = nowtime    #生成された時間
        self.changeFrag = False #速度が変化したかを表すフラグ

        self.X = targetX-self.x
        self.Y = targetY-self.y
        self.s = math.sqrt(self.X*self.X+self.Y*self.Y)

    def move(self):
        return super().move(self.X, self.Y, self.s, self.speed)
    
    def changeEyeSpeed(self, nowtime, player):
        if(self.canChangeSpeed(nowtime)):
            self.speed = self.changeSpeed
            self.X = player.x - self.x
            self.Y = player.y - self.y
            self.s = math.sqrt(self.X*self.X+self.Y*self.Y)

    #第一引数に現在のWorldTime,速度変化のクールタイムを過ぎているならTrue返す
    def canChangeSpeed(self, nowtime):        

        # まだ速度が変化していないならば
        if not self.changeFrag:
            if (nowtime - self.spawnTime) >= (self.coolTimeC * 60): # 生成後、一定時間が経過したならば
                self.changeFrag = True
                return True
        else:
            return False
            
    def hit(self, target):
        return super().hit(target, self.damage)
    
