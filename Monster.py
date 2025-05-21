from graphics import *
from Character import *
from Bar import *
from WorldTime import *
from BossSwordAttack import *
import math
class Monster(Character):
    def __init__(self, x, y, hp, maxhp, speed, damage, pixmap):
        super().__init__(x, y, hp, maxhp, speed, pixmap)
        self.damage = damage        # モンスターが与えるダメージ量
        self.cooltime = 1           # 攻撃のクールタイム
        self.beforeAttackTime = 0   # 以前攻撃したWorldTimeを保存する
        self.range = 16             # 当たり判定の広さ
        self.fattack = True         # 攻撃可能かどうかを示すTrueなら可能
        self.hpbar = HpBar(self,'red')    # モンスターのhpバー

    def move(self, player):
        X = player.x-self.x
        Y = player.y-self.y
        s = math.sqrt(X*X+Y*Y)
        dx = X/s*self.speed
        dy = Y/s*self.speed
        self.x = self.x+dx
        self.y = self.y+dy

        #hpバーは表示している前提
        self.hpbar.delateBar()
        self.hpbar = HpBar(self,'red')

        super().move(dx,dy)

    def attack(self, player, nowtime): #追加
        """第一引数にplayer,第二引数にモンスターのdamage,第三引数に現在のWorldTime"""
        self.canAttack(nowtime)
        if self.fattack:
            if super().isHit(player,self.range):
                self.fattack = False
                player.hp -= self.damage * player.defence
                self.beforeAttackTime = nowtime
                # print("hp:" + str(player.hp)) # ここでプレイヤーのhpを表示している
                # player.hit(nowtime)
    
    def canAttack(self,nowtime):    #追加
        """第一引数に現在のWorldTime,攻撃のクールタイムを過ぎているならfattackをTrueにする"""
        if not self.fattack:
            if (nowtime - self.beforeAttackTime) >= (self.cooltime * 60):
                self.fattack = True

class Gaikotsu(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, 1.0, 10, "./img/gaikotsu.png")

    def move(self, player):
        return super().move(player)
    
class Cthulhu(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, 0.5, 0,"./img/cthulhu.png")

        self.cooltimeS = 5   #魔法攻撃のクールタイム
        self.beforeShotTime = 0   #以前に魔法攻撃したWorldTimeを保存する
        self.fShot = True #魔法攻撃が可能かどうかを示す。Trueなら可能

    def move(self, player):
        return super().move(player)
    
    def canShotEye(self, nowtime):
        
        if not self.fShot:
            if (nowtime - self.beforeShotTime) >= (self.cooltimeS * 60):
                self.beforeShotTime = nowtime
                self.fShot = True
            return False
        else:
            self.fShot = False
            return True

class Wolf(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 15, 15, 2.0, 15, "./img/wolf.png")

    def move(self, player):
        return super().move(player)

class Ghost(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, 0.6, 20, "./img/ghost.png")

    def move(self, player):
        return super().move(player)
    
    def attack(self, player, nowtime):
        """第一引数にplayer,第二引数にモンスターのdamage,第三引数に現在のWorldTime"""
        self.canAttack(nowtime)
        if self.fattack:
            if super().isHit(player,self.range):
                self.fattack = False
                player.hp -= self.damage
                self.beforeAttackTime = nowtime
                # print("hp:" + str(player.hp)) # ここでプレイヤーのhpを表示している
                # player.hit(nowtime)
    
    def canAttack(self,nowtime):
        """第一引数に現在のWorldTime,攻撃のクールタイムを過ぎているならfattackをTrueにする"""
        if not self.fattack:
            if (nowtime - self.beforeAttackTime) >= (self.cooltime * 60):
                self.fattack = True

class FinalBoss(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 500, 500, 1.5, 30, "./img/boss/boss.png") # hp:500
        self.swordAttack = BossSwordAttack() # 剣エフェクトのインスタンス

    def main(self, bx, by, player, win):
        self.swordAttack.main(bx, by, player, win) # 剣による攻撃処理

    def undrawEffect(self): # 剣を削除する
        self.swordAttack.undrawSword()