from graphics import Text, Point
from Button import Button

class GameClear():
    def __init__(self):

        self.gameClearText = Text(Point(400, 400), "GameClear") # ゲームクリアのテキスト
        self.gameClearText.setSize(36)
        self.gameClearText.setStyle("bold")
        self.gameClearText.setFill("white")

        self.gameClearTimeText = Text(Point(400, 350), "") # ゲームクリア時間のテキスト
        self.gameClearTimeText.setSize(24)
        # self.gameClearTimeText.setStyle("bold")
        self.gameClearTimeText.setFill("white")

        self.returnTitleButton = Button(Point(250, 250), 150, 50, "Return to the title")
        self.quitButton = Button(Point(550, 250), 150, 50, "Exit the game")

        self.isReturnTitleClicked = False

    def showGameClear(self, timer, win):
        # ゲームオーバーの文字とボタンを表示
        self.gameClearText.draw(win)
        self.returnTitleButton.drawButton(win)
        self.quitButton.drawButton(win)

        # クリアタイムの表示
        self.gameClearTimeText.setText(f"Your Clear Time {timer.getTime()}")
        self.gameClearTimeText.draw(win)

        # ボタンが押されるまで待機
        pt = win.getMouse()
        while True:
            if(self.quitButton.isclicked(pt)): # quitButtonが押されたらゲームを終了する
                break
            if(self.returnTitleButton.isclicked(pt)):
                self.isReturnTitleClicked = True
                break

            pt = win.getMouse()
        
        # テキストやボタンを消す
        self.returnTitleButton.undrawButton()
        self.quitButton.undrawButton()
        self.gameClearText.undraw()
        self.gameClearTimeText.undraw()