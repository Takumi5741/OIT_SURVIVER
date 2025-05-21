from graphics import *
from Character import *
from Player import *
from Monster import *
from Projectile import *
from Experience import *
from Bar import *
from WorldTime import *
from GameTimer import *
from GameTitle import *
from GameClear import *
from GameOver import *
from LevelUp import *
import random
import time

def main():
    #ウィンドウの初期設定
    width = 800 # ウィンドウの横サイズ
    height = 600 # ウィンドウの縦サイズ
    win = GraphWin("OIT Survivor", width, height, autoflush=False)
    win.setCoords(0, 0, width, height)

    gameTitle = GameTitle()
    gameTitle.showGameStart(win)
    if(gameTitle.isContinueClicked == False):
        win.close()
    gameTitle.isContinueClicked = False

    #背景の描画
    Image(Point(400,300), "img/background.png").draw(win)

    flag = True

    while flag:

        # ゲームクリア＆ゲームオーバー処理インスタンスの作成
        gameClear = GameClear()
        gameOver = GameOver()

        # 世界時間の初期化
        worldTime = WorldTime()

        # タイマーのインスタンス作成
        timer = GameTimer(win)

        # キャラクターの配置
        player = Player(400, 300)
        player.draw(win)
        playerHpBar = createHpBar(player,win,'cyan')

        #経験値バー
        experienceBar = ExperienceBar(50,570,700,player)
        experienceBar.createBar(win)

        magicfireList = [] # worldに存在する複数のmagicFireを管理する配列
        monsterprj = [] #モンスターの飛び道具を管理する配列
        monsterList = [] # worldに存在するモンスターを管理する配列
        experienceList = [] #worldに存在する複数のExperienceを詰め込む配列
        levelupList = ['hp', 'speed', 'defence','bullets', 'sword']    #レベルアップの選択肢

        experienceLimit = 30 # 追加 存在できる経験値の最大数

        # ボスを倒したかどうかのフラグ
        isBossDefeated = False
        isBossExist = False
        inGameFlag = True
        
        while inGameFlag:
            # 世界時間を進める
            worldTime.advanceTime()

            # プレイヤーの移動処理
            player.move(win.checkMouse())
            playerHpBar.delateBar()
            playerHpBar = createHpBar(player,win,'cyan')

            # 青い魔法の飛び道具の処理
            if(player.canShotFire(worldTime.getTime())):# もしmagicFireが放てるならば

                # gaikotsuListが空でない(敵が少なくとも一体は存在する)ならば
                if len(monsterList) > 0:

                    shotFireEvent(magicfireList, monsterList, player.maxFire, player, win)

            # magicfireを動かす
            for i in magicfireList:
                i.move()

                # 全ての敵を探索し、magicfireが衝突しているかを判定
                for j in monsterList:
                    i.hit(j)

                # 追加 機能しないmagicfireのインスタンスを廃棄する
                if not i.canUse():
                    i.undraw()
                    magicfireList.remove(i) # magicfireListから、該当する飛び道具のインスタンスを排除する

            # モンスターの飛び道具を動かす
            for i in monsterprj:
                i.move()
                i.hit(player)   #プレイヤーに当たっているかを判定

                if type(i) is Eye: #目玉の場合
                    i.changeEyeSpeed(worldTime.getTime(), player)
            
                if not i.canUse():
                    i.undraw()
                    monsterprj.remove(i) # monsterprjから、該当する飛び道具のインスタンスを排除する
        

            # 剣の攻撃処理
            player.sword.main(player.x, player.y, monsterList, win)

            #モンスターの処理
            for monster in monsterList:
                monster.move(player) # モンスターの移動
                monster.hpbar.createBar(win)

                if type(monster) is Gaikotsu:#ガイコツの場合
                    monster.attack(player, worldTime.getTime()) # モンスターの攻撃
                
                elif type(monster) is Wolf:#オオカミの場合
                    monster.attack(player, worldTime.getTime()) # モンスターの攻撃

                elif type(monster) is Ghost:#ゴーストの場合
                    monster.attack(player, worldTime.getTime()) # モンスターの攻撃                

                elif type(monster) is Cthulhu:#タコの場合
                    if(monster.canShotEye(worldTime.getTime())):

                        eye = Eye(monster.x, monster.y, player.x, player.y, worldTime.getTime())
                        monsterprj.append(eye)
                        j = (len(monsterprj)-1)      # j = 配列の長さ - 1 (配列の最後尾の添え字)
                        monsterprj[j].draw(win)      # 追加したインスタンスを描画する

                elif type(monster) is FinalBoss: # ボスの場合
                    monster.attack(player, worldTime.getTime()) # モンスターの攻撃
                    monster.main(boss.x, boss.y, player, win) # ボス特有の攻撃

                if(monster.isDead()): # モンスターの死亡判定
                    if(type(monster) is FinalBoss):
                        monster.undraw()
                        monster.undrawEffect() # ボスの剣エフェクトを削除する
                        monster.hpbar.delateBar()
                        isBossDefeated = True
                    else:
                        monster.undraw()
                        monster.hpbar.delateBar()
                        experienceSpawn(experienceList,win,monster,worldTime.getTime()) #経験値を落とす
                        monsterList.remove(monster)
            
            #経験値の獲得
            for experience in experienceList:
                experience.gainExperience(player)
                experience.despawnCheck(worldTime.getTime()) #追加
                if experience.isDead():
                    experience.undraw()
                    experienceList.remove(experience)

            #プレイヤーのレベルアップ
            if player.canLevelUp():
                experienceBar.changeBar(player, win)
                time.sleep(0.3)
                lvList = random.sample(levelupList,3)   #レベルアップの選択肢からランダムに3つ選ぶ
                levelUp(chooseLevelUp(lvList,win),player)   #レベルアップ時のGUI処理

            else:
                experienceBar.changeBar(player, win)
            
            if player.sword.level >= 3 and 'sword' in levelupList: # 剣のレベルが3になったらlevelUpListの中からswordの選択肢を消す
                levelupList.remove('sword')
            if player.magicPowerLevel >= 3 and 'bullets' in levelupList:
                levelupList.remove('bullets')
                
            # プレイヤーの死亡判定
            if player.isDead():
                player.undraw()
                for mf in magicfireList: # 現在表示されている魔法の飛び道具を削除
                    mf.undraw()

                inGameFlag = False
            command = win.checkKey()
            if command=='q':
                player.dead = True
            if command=='h':
                player.heal()
            if command=='p':
                win.getMouse()
            if command=='l':
                player.experience = player.maxexperience
            if command=='t':
                worldTime.advanceTime1()
            # if command=='b':
            #     boss = FinalBoss(800 + 40, 600 + 30)
            #     boss.draw(win)      # 追加したインスタンスを描画する
            #     boss.hpbar.createBar(win)
            #     monsterList.append(boss)
            
            #モンスターをスポーンさせる
            limit,wave = monsterSpawnLimit(worldTime.getTime())
            monsterSpawnEvent(monsterList, limit, win, player,wave)
            
            experienceSpawnLimit(experienceList,experienceLimit)# 追加

            # ボスのスポーン
            if isBossExist == False:
                if worldTime.getTime() >= 18000: # 5分(18000)を超えたらBossを出現させる
                    boss = FinalBoss(800 + 40, 600 + 30)
                    boss.draw(win)      # 追加したインスタンスを描画する
                    boss.hpbar.createBar(win)
                    monsterList.append(boss)
                    isBossExist = True

            # ボスを倒したかどうか
            if(isBossDefeated == True):
                player.undraw()
                for mf in magicfireList: # 現在表示されている魔法の飛び道具を削除
                    mf.undraw()
                inGameFlag = False

            # 経過時間の処理
            timer.main(worldTime.getTime(), win)

            update(60)

        #ゲームクリア＆ゲームオーバー処理
        if(isBossDefeated == True):
            gameClear.showGameClear(timer, win)
        else:
            gameOver.showGameOver(win)

        if(gameClear.isReturnTitleClicked or gameOver.isReturnTitleClicked):
            gameTitle.showGameStart(win)
            if(gameTitle.isContinueClicked):
                gameTitle.isContinueClicked = False
                for monster in monsterList: # 現在表示されているモンスターを削除
                    monster.undraw()
                    monster.hpbar.delateBar()
                    if(type(monster) is FinalBoss):
                        monster.undrawEffect() # ボスの剣エフェクトを削除する
                    
                for experience in experienceList:   #現在表示されている経験値を削除
                    experience.undraw()

                for prj in monsterprj:              #モンスターの飛び道具を削除
                    prj.undraw()

                timer.undrawTimer()
                experienceBar.delateBar()
                playerHpBar.delateBar()

                #インスタンスを削除
                for monster in monsterList:
                    monsterList.remove(monster)
                for magicfire in magicfireList:
                    magicfireList.remove(magicfire)
                for prj in monsterprj:
                    monsterprj.remove(prj)
                for experience in experienceList:
                    experienceList.remove(experience)
            else:
                break
        else:
            break # ゲームを終了する

    win.close()

#playerが撃てるmagicFireの個数を受け取り、インスタンスを生成してmagicfireListに格納するメソッド
def shotFireEvent(magicfireList, monsterList, maxFire, player, win):

    if len(monsterList) > 0:
        # sortedList = sorted(monsterList, key=getDistance())
        for i in range(0, len(monsterList)-1):
            mindex = i
            X = player.x-monsterList[mindex].x
            Y = player.y-monsterList[mindex].y
            ms = math.sqrt(X*X+Y*Y)

            for j in range(i, len(monsterList)-1):
                X = player.x-monsterList[j].x
                Y = player.y-monsterList[j].y
                s = math.sqrt(X*X+Y*Y)
                if ms > s:
                    # 敵が画面内に居るなら選ぶ
                    if (0 <= monsterList[j].x < 800 and 0 <= monsterList[j].y < 600):
                        mindex = j
            tmp = monsterList[i]
            monsterList[i] = monsterList[mindex]
            monsterList[mindex] = tmp
        
        i = 0
        while i < maxFire and i < len(monsterList):
            # magicfire(飛び道具)のインスタンスを作成
            magicfire = magicFire(player.x, player.y, monsterList[i].x, monsterList[i].y, player.msRate, player.maRate)

            magicfireList.append(magicfire) # magicfireListの最後尾にインスタンスを追加
            j = (len(magicfireList)-1)      # j = 配列の長さ - 1 (配列の最後尾の添え字)
            magicfireList[j].draw(win)      # 追加したインスタンスを描画する
            i += 1

# [更新]
# 世界時間に応じて、スポーンできるモンスターの最大数とウェーブの段階(1~5)を決めて返す。
def monsterSpawnLimit(nowTime):
    max =  2*(int(nowTime/1800)+1)
    if nowTime <= 3600: # 1分までの場合
        return max,1
    elif nowTime <= 7200: # 2分までの場合
        return max,2
    elif nowTime <= 10800: # 3分までの場合
        return max,3
    elif nowTime <= 14400: # 4分までの場合
        return max,4
    else :                # 5分以降
        return max,5
    
    # if nowTime <= 1800: # 30秒までの場合
    #     return 1
    # elif nowTime <= 3600: # 1分までの場合
    #     return 10
    # else :
    #     return 30
    
# [更新]    
# スポーンできるモンスターの最大数とウェーブ数を基に、MonsterListにモンスターを追加する。
def monsterSpawnEvent(monsterList, limit, win, player, wave):
    
    if len(monsterList) < limit:
        for i in range(len(monsterList) ,limit):
            late = random.random()
            if late < 0.2:  # 20%の確率で実行
                p_x,p_y = player.x,player.y # プレイヤーの座標取得
                x, y = SpawnCoordinate(p_x, p_y)    # プレイヤーの座標に応じてランダムな座標を取得

                # [更新]waveの値に応じて出現する敵の種類と割合を決定する 
                #敵のスポーン率
                late2 = random.random()
                if wave == 1:
                    gaikotsu = Gaikotsu(x,y)
                    monsterList.append(gaikotsu)

                elif wave == 2:
                    if late2 < 0.9: # ガイコツ
                        gaikotsu = Gaikotsu(x,y)
                        monsterList.append(gaikotsu)
                    elif late2 < 1: # タコ
                        cthulhu = Cthulhu(x,y)
                        monsterList.append(cthulhu)

                elif wave == 3:
                    if late2 < 0.7: # ガイコツ
                        gaikotsu = Gaikotsu(x,y)
                        monsterList.append(gaikotsu)
                    elif late2 < 0.9: # タコ
                        cthulhu = Cthulhu(x,y)
                        monsterList.append(cthulhu)
                    elif late2 < 1: #オオカミ
                        wolf = Wolf(x,y)
                        monsterList.append(wolf)

                elif wave == 4:
                    if late2 < 0.4: # ガイコツ
                        gaikotsu = Gaikotsu(x,y)
                        monsterList.append(gaikotsu)
                    elif late2 < 0.7: # タコ
                        cthulhu = Cthulhu(x,y)
                        monsterList.append(cthulhu)
                    elif late2 < 0.9: #オオカミ
                        wolf = Wolf(x,y)
                        monsterList.append(wolf)
                    elif late2 < 1: #ゴースト
                        ghost = Ghost(x,y)
                        monsterList.append(ghost)
                else :
                    if late2 < 0.2: # ガイコツ
                        gaikotsu = Gaikotsu(x,y)
                        monsterList.append(gaikotsu)
                    elif late2 < 0.5: # タコ
                        cthulhu = Cthulhu(x,y)
                        monsterList.append(cthulhu)
                    elif late2 < 0.8: #オオカミ
                        wolf = Wolf(x,y)
                        monsterList.append(wolf)
                    elif late2 < 1: #ゴースト
                        ghost = Ghost(x,y)
                        monsterList.append(ghost)


                j = (len(monsterList)-1)      # j = 配列の長さ - 1 (配列の最後尾の添え字)
                monsterList[j].draw(win)      # 追加したインスタンスを描画する
                monsterList[j].hpbar.createBar(win)

            # late = random.random()
            # if late < 0.2:  # 20%の確率で実行

            #     p_x,p_y = player.x,player.y # プレイヤーの座標取得
            #     x, y = SpawnCoordinate(p_x, p_y)    # プレイヤーの座標に応じてランダムな座標を取得
            #     gaikotsu = Gaikotsu(x,y)
            #     monsterList.append(gaikotsu)
            #     j = (len(monsterList)-1)      # j = 配列の長さ - 1 (配列の最後尾の添え字)
            #     monsterList[j].draw(win)      # 追加したインスタンスを描画する
            #     monsterList[j].hpbar.createBar(win)

# 敵がスポーンする座標をランダムに返すメソッド
def SpawnCoordinate(p_x, p_y):
    distance = 600

    # プレイヤーの座標を中心としたフィールドの範囲
    field_min_x = p_x - distance
    field_max_x = p_x + distance
    field_min_y = p_y - distance
    field_max_y = p_y + distance

    # 画面範囲
    screen_min_x = 0
    screen_max_x = 800
    screen_min_y = 0
    screen_max_y = 600

    # モンスターの出現領域を決定
    while True:
        # モンスターの出現座標をランダムに選択
        if random.choice([True, False]):  # x方向にdistance離れる
            m_x = random.choice([field_min_x - 1, field_max_x + 1])
            m_y = random.randint(screen_min_y, screen_max_y - 1)
        else:  # y方向にdistance離れる
            m_y = random.choice([field_min_y - 1, field_max_y + 1])
            m_x = random.randint(screen_min_x, screen_max_x - 1)

        # 出現位置が画面外の場合、確定
        if not (screen_min_x <= m_x < screen_max_x and screen_min_y <= m_y < screen_max_y):
            return m_x, m_y

#経験値を表示させるメソッド
def experienceSpawn(experienceList, win, monster, nowtime):
    experience = Experience(monster.x,monster.y, nowtime,"./img/experience.png",1)
    experienceList.append(experience)
    experienceList[len(experienceList)-1].draw(win)

#追加 経験値のインスタンスが最大数を超えた場合に、最も古い経験値を削除するメソッド
def experienceSpawnLimit(experienceList, experienceLimit): 
    if(len(experienceList) > experienceLimit):
        experienceList[0].despawn()

#hpバーを表示させるメソッド
def createHpBar(target, win,color):
    hpBar = HpBar(target,color)
    hpBar.createBar(win)
    return hpBar

main()