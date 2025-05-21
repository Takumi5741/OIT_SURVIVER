from graphics import *

class Sword():

    def __init__(self, point):
        self.imgList = [None] * 10 # アニメーション用の画像リスト
        self.img_smallList = [] # 剣エフェクト(小)の画像リスト
        self.img_normalList = [] # 剣エフェクト(中)の画像リスト
        self.img_largeList = [] # 剣エフェクト(大)の画像リスト

        for n in range(0,10):
            self.img_smallList.append(Image(point, f"img/sword/small/sword{n+1}.png")) # 192×96の画像
            self.img_normalList.append(Image(point, f"img/sword/normal/sword{n+1}.png")) # 240×120の画像
            self.img_largeList.append(Image(point, f"img/sword/large/sword{n+1}.png")) # 288×144の画像

            self.imgList[n] = self.img_smallList[n]
            
        self.width = 192 # 横の当たり判定 (初期: 192)
        self.height = 96 # 縦の当たり判定 (初期: 96)
        self.attackRangeRatio = 1.0
        self.damage = 10 # 剣が与えるダメージ量 (初期: 10?)
        self.damageRatio = 1.0
        self.coolTime = 60 # 次の攻撃を出すまでの時間（初期: 60）
        self.coolTimeRatio = 1.0
        self.level = 1 # レベル(初期: 1)
        self.wantToLevelUp = False # レベルアップするかどうか
        self.tick = 1

    def main(self, px, py, monsterList, win):

        if(self.tick >= 2 and self.tick <= 11):
            self.imgList[self.tick-2].undraw()
        if(self.tick >= 1 and self.tick <= 10):
            self.imgList[self.tick-1].move(px - self.imgList[self.tick-1].getAnchor().getX(), py - self.imgList[self.tick-1].getAnchor().getY() + 32)
            self.imgList[self.tick-1].draw(win)

        # 攻撃処理
        if(self.tick == 1):
            for monster in monsterList:
                if (abs(self.imgList[self.tick-1].getAnchor().getX() - monster.x) < ((self.width * self.attackRangeRatio) / 2 + monster.getWidth() / 2)
                    and abs(self.imgList[self.tick-1].getAnchor().getY() - monster.y) < ((self.height * self.attackRangeRatio) / 2 + monster.getHeight() / 2)):
                    monster.hp -= int(self.damage * self.damageRatio) # monsterの体力を減らす
        
        self.tick += 1
        # レベルアップ処理
        if (self.wantToLevelUp == True and self.tick == int(self.coolTime * self.coolTimeRatio) + 1):
            self.levelUp()
            self.wantToLevelUp = False

        if self.tick >= int(self.coolTime * self.coolTimeRatio) + 1:
            self.tick = 1
    
    def levelUp(self):
        self.level += 1

        if (self.level == 2):
            for i in range(0, 10):
                self.imgList[i] = self.img_normalList[i]
            self.attackRangeRatio = 1.25
            self.damageRatio = 1.25
            self.coolTimeRatio = 0.75
        elif (self.level == 3):
            for i in range(0, 10):
                self.imgList[i] = self.img_largeList[i]
            self.attackRangeRatio = 1.5
            self.damageRatio = 1.5
            self.coolTimeRatio = 0.5

    def undrawSword(self):
        for img in self.imgList:
            img.undraw()