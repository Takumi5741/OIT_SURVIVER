from graphics import *
from Character import *
from Sword import *
import math
class Player(Character):
    def __init__(self, x, y):
        # プレイヤーの立ち絵の生成
        super().__init__(x, y, 100, 100, 2.0, "./img/player.png") # HP:100, MAXHP:100, Speed: 4.0

        # 剣インスタンスの生成
        self.sword = Sword(Point(x, y))

        self.defence = 1.0  #防御係数

        self.experience = 0 #経験値
        self.maxexperience = 4 #貯められる最大経験値(これは初期値)

        self.level = 1  #レベル
        self.hpLevel = 1
        self.speedLevel = 1
        self.defenceLevel = 1
        self.magicPowerLevel = 1

        self.cooltimeF = 1   #魔法攻撃のクールタイム
        self.beforeFireTime = 0   #以前に魔法攻撃したWorldTimeを保存する
        self.fFire = True #魔法攻撃が可能かどうかを示す。Trueなら可能
        self.maxFire = 1    #プレイヤーが一度に撃てるmagicfireの個数
        self.maRate = 1     #魔法攻撃の倍率
        self.msRate = 1   #魔法速度の倍率

        self.range = 16 #hpバーのために無理やり作成

        self.movePoint = None
        self.dx = 0
        self.dy = 0

    def move(self, point):
        if point != None:
            self.movePoint = point
            X = self.movePoint.x-self.x
            Y = self.movePoint.y-self.y
            s = math.sqrt(X*X+Y*Y)
            self.dx = X/s*self.speed
            self.dy = Y/s*self.speed
        if not (self.movePoint != None and super().isHit(self.movePoint,self.speed)):
            self.x = self.x+self.dx
            self.y = self.y+self.dy
            return super().move(self.dx, self.dy)

    def canLevelUp(self):
        """playerがレベルアップできるならレベルアップしてTrueを返す"""
        if self.experience >= self.maxexperience:
            self.level += 1
            self.experience -= self.maxexperience   #レベルアップに必要な経験値を引く
            self.maxexperience = 4 * self.level    #レベルアップ後の貯められる最大経験値
            return True
        else:
            return False

    # 魔法攻撃
    def canShotFire(self, nowtime):
        """第一引数に現在のWorldTime,攻撃のクールタイムを過ぎているならfFireをTrueにする"""
        
        if not self.fFire:
            if (nowtime - self.beforeFireTime) >= (self.cooltimeF * 60):
                self.beforeFireTime = nowtime
                self.fFire = True
            return False
        else:
            self.fFire = False
            return True 

    # プレイヤーやアイテムの削除
    def undraw(self):
        super().undraw()
        self.sword.undrawSword()

    # 魔法攻撃のステータスを上昇させる。レベルアップ時に実行
    def magicPowerUp(self):
        self.maxFire += 1
        self.maRate += 0.25
        self.msRate += 0.25
        self.magicPowerLevel += 1

    def heal(self):
        self.hp = self.maxhp