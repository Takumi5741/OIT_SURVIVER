from graphics import Point
from Button import Button

def chooseLevelUp(choices,win):
    """選択肢を表示させる"""
    cnt = 0
    x , y = 400, 400
    w , h = 400, 100
    buttonList = [] #表示させるボタンを管理するList
    buttonDictionary = {}   #キーをボタン番号、値を選択肢の名前にしている

    for choice in choices:
        if choice == 'hp':
            buttonList.append(Button(Point(x,y-(h*cnt)), w, h, 'HP'))
            buttonList[cnt].drawButton(win)
            buttonDictionary[cnt] = 'hp'
            cnt += 1
        elif choice == 'speed':
            buttonList.append(Button(Point(x,y-(h*cnt)), w, h, 'SPEED'))
            buttonList[cnt].drawButton(win)
            buttonDictionary[cnt] = 'speed'
            cnt += 1
        elif choice == 'defence':
            buttonList.append(Button(Point(x,y-(h*cnt)), w, h, 'DEFENCE'))
            buttonList[cnt].drawButton(win)
            buttonDictionary[cnt] = 'defence'
            cnt += 1
        elif choice == 'bullets':
            buttonList.append(Button(Point(x,y-(h*cnt)), w, h, 'MAGIC FIRE'))
            buttonList[cnt].drawButton(win)
            buttonDictionary[cnt] = 'bullets'
            cnt += 1
        elif choice == 'sword':
            buttonList.append(Button(Point(x,y-(h*cnt)), w, h, 'SWORD'))
            buttonList[cnt].drawButton(win)
            buttonDictionary[cnt] = 'sword'
            cnt += 1

    while True:
        pt = win.getMouse()
        for i in range(cnt):
            if buttonList[i].isclicked(pt):
                for j in range(cnt):    #全てのボタンを非表示
                    buttonList[j].undrawButton()
                return buttonDictionary[i]  #押されたボタンの名前を返す
            
def levelUp(choice, player):
    """選んだ選択肢ごとの処理"""
    if choice == 'hp':
            addhp = 20 + player.maxhp/10
            player.maxhp += addhp
            player.hp += addhp
            player.hpLevel += 1

    elif choice == 'speed':
        player.speed += 0.2 + player.speed/10
        player.speedLevel += 1
        
    elif choice == 'defence':
        player.defence = player.defence*0.8
        player.defenceLevel += 1
    
    elif choice == 'sword':
        player.sword.wantToLevelUp = True
        print(str(player.sword.level))

# 追加 magicFireの強化
    elif choice == 'bullets':
        player.magicPowerUp()
        print(str(player.magicPowerLevel))
