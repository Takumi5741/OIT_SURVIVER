from graphics import *
from Character import *

class Experience(Character):
    def __init__(self, x, y, spawntime, pixmap,value): #変更 spawntimeを追加
        super().__init__(x, y, 0, 0, 0, pixmap)

        self.spawntime = spawntime # 追加
        self.despawntime = 30   # 追加 存在できる時間

        self.hp = 1
        self.value = value
        self.range = 25

    def gainExperience(self,player):
        """playerに経験値を渡して、isDeadをTrueにする"""
        if super().isHit(player,self.range):
            player.experience += self.value
            self.hp = 0
            super().isDead()

    #追加 生成されてから一定時間経った経験値を消す
    def despawnCheck(self,nowtime):
        if(nowtime - self.spawntime >= self.despawntime * 60):
            self.hp = 0
            super().isDead()

    def despawn(self):
        self.hp = 0
        super().isDead()