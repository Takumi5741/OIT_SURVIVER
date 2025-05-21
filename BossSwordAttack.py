from graphics import *

class BossSwordAttack():

    def __init__(self):
        self.img_normalList = [] # 剣エフェクト(中)の画像リスト
        self.img_normal_reverseList = [] #剣エフェクト（中）下向きの画像リスト

        for n in range(0,10):
            self.img_normalList.append(Image(Point(0,0), f"img/sword/normal/sword{n+1}.png")) # 240×120の画像
            self.img_normal_reverseList.append(Image(Point(0,0), f"img/sword/normal/sword{n+1}_reverse.png")) # 240×120の画像
        
        # 剣エフェクトをインスタンス化
        self.swordAttackUpper = BossSword(self.img_normalList, 0, 32)
        self.swordAttackLower = BossSword(self.img_normal_reverseList, 30, -32)

    def main(self, bx, by, player, win):

        self.swordAttackUpper.main(bx, by, player, win) # 剣エフェクト（上）の処理
        self.swordAttackLower.main(bx, by, player, win) # 剣エフェクト（下）の処理

    def undrawSword(self): # 剣エフェクトを削除
        self.swordAttackUpper.undrawSword()
        self.swordAttackLower.undrawSword()

class BossSword():
    # example = BossSword(imgList:[String], seed:int, yPosition:int)

    def __init__(self, imgList, seed, yPosition):
        self.img_swordList = []

        for img in imgList:
            self.img_swordList.append(img)

        self.width = 240 # 横の当たり判定
        self.height = 120 # 縦の当たり判定
        self.damage = 30 # 剣が与えるダメージ量
        self.damageRatio = 1.0
        self.coolTime = 180 # 次の攻撃を出すまでの時間
        self.coolTimeRatio = 1.0
        self.tick = 0 + seed # シード値
        self.yPosition = yPosition # 剣のエフェクトを出すy位置
    
    def main(self, bx, by, player, win):

        # 剣のアニメーション
        if(self.tick >= 2 and self.tick <= len(self.img_swordList) + 1):
            self.img_swordList[self.tick-2].undraw()
        if(self.tick >= 1 and self.tick <= len(self.img_swordList)):
            self.img_swordList[self.tick-1].move(bx - self.img_swordList[self.tick-1].getAnchor().getX(), by - self.img_swordList[self.tick-1].getAnchor().getY() + self.yPosition)
            self.img_swordList[self.tick-1].draw(win)

        # # 攻撃処理
        if(self.tick == 1):
            if (abs(self.img_swordList[self.tick-1].getAnchor().getX() - player.x) < (self.width / 2 + player.getWidth() / 2)
                and abs(self.img_swordList[self.tick-1].getAnchor().getY() - player.y) < (self.height / 2 + player.getHeight() / 2)):
                player.hp -= int(self.damage * self.damageRatio*player.defence)

        self.tick += 1

        if self.tick >= self.coolTime + 1:
            self.tick = 1
    
    def undrawSword(self):
        for img in self.img_swordList:
            img.undraw()